import {Bucket} from "@aws-cdk/aws-s3";
import {CfnOutput, Construct} from "@aws-cdk/core";
import {LambdaRestApi} from "@aws-cdk/aws-apigateway";
import {Code, Function as LambdaFunction} from "@aws-cdk/aws-lambda";
import {Runtime} from "@aws-cdk/aws-lambda";

export class EduaceBackend extends Construct {
    constructor(scope: Construct, id: string) {
        super(scope, id);

        const sourceCodeBucket = new Bucket(this, "EduaceBackendLambdaStore")

        new CfnOutput(this, "EduaceBackendLambdaStoreARNOutput", {
            exportName: "S3BackendCodeBucketArn",
            value: sourceCodeBucket.bucketArn
        })

        const lambdaFunction = new LambdaFunction(this, "EduaceBackendLambdaFunction", {
            runtime: Runtime.PYTHON_3_9,
            // Code may not exist at infra build time
            code: Code.fromBucket(sourceCodeBucket, "build.zip"),
            // Name of the method that we call in the Python code
            handler: "main", // TODO: Check this in the code!
            environment: {
                FLASK_DEBUG: "false"
            }
        })

        sourceCodeBucket.grantRead(lambdaFunction) // This might not be necessary

        // Using the LambdaRestApi means that all API requests are piped to the lambda function
        const apiGateway = new LambdaRestApi(this, "EduaceBackendAPIGateway", {
            handler: lambdaFunction,
            restApiName: "EduaceBackendAPIGateway",
            description: "API Gateway for Eduace API"
        })
    }
}