import {Aws, CfnOutput, Construct, Stack} from "@aws-cdk/core";
import {Bucket} from "@aws-cdk/aws-s3";
import {ARecord, HostedZone, RecordTarget} from "@aws-cdk/aws-route53";
import {DnsValidatedCertificate} from "@aws-cdk/aws-certificatemanager";
import {
    CloudFrontAllowedMethods,
    CloudFrontWebDistribution,
    OriginAccessIdentity,
    SecurityPolicyProtocol,
    SSLMethod,
    ViewerCertificate
} from "@aws-cdk/aws-cloudfront";
import {Metric} from "@aws-cdk/aws-cloudwatch";
import {CanonicalUserPrincipal, PolicyStatement} from "@aws-cdk/aws-iam";
import {CloudFrontTarget} from "@aws-cdk/aws-route53-targets";

export class EduaceFrontend extends Construct {
    constructor(scope: Stack, id: string, domainName: string) {
        super(scope, id);

        const frontendBucket = new Bucket(this, "FrontendBucket", {
            bucketName: domainName,
            websiteIndexDocument: "index.html",
            websiteErrorDocument: "error.html",
            publicReadAccess: false,
        })

        new CfnOutput(this, "EduaceFrontendSiteBucketARN", {
            exportName: "S3FrontendCodeBucketARN",
            value: frontendBucket.bucketArn
        })

        const cloudfrontOAI = new OriginAccessIdentity(this, 'FrontendCFOAI', {
            comment: `OAI for ${id}`
        });

        frontendBucket.addToResourcePolicy(new PolicyStatement({
            actions: ['s3:GetObject'],
            resources: [frontendBucket.arnForObjects('*')],
            principals: [new CanonicalUserPrincipal(cloudfrontOAI.cloudFrontOriginAccessIdentityS3CanonicalUserId)]
        }));

        const hostedZone = HostedZone.fromLookup(this, "EduaceZone", {
            domainName: domainName
        })

        const tlsCertificate = new DnsValidatedCertificate(this, "EduaceFrontendCertificate", {
            domainName: domainName,
            hostedZone: hostedZone,
            region: "us-east-1", // Cloudfront only checks this region for certificates.
        })

        const viewerTlsCertificate = ViewerCertificate.fromAcmCertificate(tlsCertificate, {
            sslMethod: SSLMethod.SNI,
            securityPolicy: SecurityPolicyProtocol.TLS_V1_1_2016,
            aliases: [domainName]
        })

        const cloudfrontDistribution = new CloudFrontWebDistribution(this, "EduaceCloudfrontDistribution", {
            viewerCertificate: viewerTlsCertificate,
            originConfigs: [{
                s3OriginSource: {
                    s3BucketSource: frontendBucket,
                    originAccessIdentity: cloudfrontOAI
                },
                behaviors: [{
                    isDefaultBehavior: true,
                    compress: true,
                    allowedMethods: CloudFrontAllowedMethods.GET_HEAD_OPTIONS
                }]
            }],
            errorConfigurations: [{
                errorCode: 403,
                errorCachingMinTtl: 0,
                responseCode: 200,
                responsePagePath: "/index.html"
            }]
        });

        new CfnOutput(this, "EduaceFrontendDistributionURL", {
            exportName: "EduaceFrontendDistributionURL",
            value: cloudfrontDistribution.distributionDomainName
        })

        new ARecord(this, "EduaceFrontendARecord", {
            recordName: domainName,
            target: RecordTarget.fromAlias(new CloudFrontTarget(cloudfrontDistribution)),
            zone: hostedZone
        })
    }
}
