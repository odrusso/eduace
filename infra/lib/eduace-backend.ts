import {CfnOutput, Construct} from "@aws-cdk/core";
import {Peer, Port, SecurityGroup, Vpc} from "@aws-cdk/aws-ec2";
import {
    Cluster,
    Compatibility,
    FargateService,
    LogDriver,
    NetworkMode,
    RepositoryImage,
    TaskDefinition
} from "@aws-cdk/aws-ecs";
import {
    ApplicationLoadBalancer,
    ApplicationProtocol,
    ApplicationTargetGroup,
    Protocol,
    TargetType
} from "@aws-cdk/aws-elasticloadbalancingv2";
import {Effect, Policy, PolicyStatement, Role, ServicePrincipal} from "@aws-cdk/aws-iam";
import {Repository} from "@aws-cdk/aws-ecr";
import {ARecord, HostedZone, RecordTarget} from "@aws-cdk/aws-route53";
import {LoadBalancerTarget} from "@aws-cdk/aws-route53-targets";

export class EduaceBackend extends Construct {
    constructor(scope: Construct, id: string, domainName: string) {
        super(scope, id);

        const defaultVpc = Vpc.fromLookup(this, 'VPC', {
            isDefault: true
        })

        const cluster = new Cluster(this, "EduaceAPICluster", {
            vpc: defaultVpc
        })

        const loadBalancer = new ApplicationLoadBalancer(this, "EduaceAPILoadBalancer", {
            vpc: defaultVpc,
            vpcSubnets: {subnets: defaultVpc.publicSubnets},
            internetFacing: true
        })

        const targetGroup = new ApplicationTargetGroup(this, "EduaceAPITaskTargetGroup", {
            port: 80,
            vpc: defaultVpc,
            protocol: ApplicationProtocol.HTTP,
            targetType: TargetType.IP
        })

        // TODO: This isn't a real health-check, but it should be indicative while the API has no external deps
        targetGroup.configureHealthCheck({
            path: "/api/v1/questions",
            protocol: Protocol.HTTP
        })

        const targetGroupListener = loadBalancer.addListener("HttpListener", {
            open: true,
            port: 80,
        })

        targetGroupListener.addTargetGroups("HttpListenerTarget", {
            targetGroups: [targetGroup]
        })

        const loadBalancerSecurityGroup = new SecurityGroup(this, "EduaceAPILoadBalancerSecurityGroup", {
            vpc: defaultVpc,
            allowAllOutbound: true
        })

        loadBalancerSecurityGroup.addIngressRule(
            Peer.anyIpv4(),
            Port.tcp(80),
            "Allow http traffic"
        )

        loadBalancer.addSecurityGroup(loadBalancerSecurityGroup)

        // TODO Make this public, because you get 100x more for free.
        // It's not like the code is closed source
        const containerRegistry = new Repository(this, "EduaceAPIContainerRepository")

        const taskRole = new Role(this, "EduaceAPITaskRole", {
            assumedBy: new ServicePrincipal("ecs-tasks.amazonaws.com"),
            roleName: "eduace-api-task-role",
            description: "Role assumed by API task"
        })

        taskRole.attachInlinePolicy(
            new Policy(this, "EduaceAPITaskECRFetchPolicy", {
                statements: [
                    // TODO: Tighten this up, a lot.
                    // We should have enough context here to allow only pulling from the specific repo we want
                    new PolicyStatement({
                        effect: Effect.ALLOW,
                        actions: ["ECR:*"],
                        resources: ["*"]
                    })
                ]
            })
        )

        const taskDefinition = new TaskDefinition(this, "EduaceAPITaskDef", {
            compatibility: Compatibility.FARGATE,
            family: "task",
            cpu: "256", // this is 0.25 of a single vCPU core, we probably want more, but it isn't free!
            memoryMiB: "512", // same concern as above
            networkMode: NetworkMode.AWS_VPC,
            taskRole: taskRole
        })

        const container = taskDefinition.addContainer("EduaceAPIContainer", {
            image: RepositoryImage.fromEcrRepository(containerRegistry, "latest"),
            memoryLimitMiB: 512,
            logging: LogDriver.awsLogs({streamPrefix: "eduace-api-logs"})
        })

        container.addPortMappings({containerPort: 80})

        const ecsService = new FargateService(this, "EduaceAPIService", {
            cluster: cluster,
            desiredCount: 1, // not very highly available, but hey, it's cheap
            taskDefinition: taskDefinition,
            securityGroups: [loadBalancerSecurityGroup],
            assignPublicIp: true // we need this to be able to reach ECR
        })

        ecsService.attachToApplicationTargetGroup(targetGroup)

        // This where where we need to push our built images to
        new CfnOutput(this, "EduaceAPIECRRepoOutput", {
            exportName: "EduaceAPIECRRepo",
            value: containerRegistry.repositoryArn
        })

        // This is the service we need to call forceRedeploy on to update the container image
        new CfnOutput(this, "EduaceAPIServiceOutput", {
            exportName: "EduaceAPIServiceARN",
            value: ecsService.serviceArn
        })

        const hostedZone = HostedZone.fromLookup(this, "EduaceAPIZone", {
            domainName: domainName
        })

        new ARecord(this, "EduaceBackendARecord", {
            recordName: "api",
            target: RecordTarget.fromAlias(new LoadBalancerTarget(loadBalancer)),
            zone: hostedZone
        })

    }
}