import {Bucket} from "@aws-cdk/aws-s3";
import {CfnOutput, Construct} from "@aws-cdk/core";
import {LambdaRestApi} from "@aws-cdk/aws-apigateway";
import {Code, Function as LambdaFunction} from "@aws-cdk/aws-lambda";
import {Runtime} from "@aws-cdk/aws-lambda";

export class EduaceBackend extends Construct {
    constructor(scope: Construct, id: string) {
        super(scope, id);

        // It's unclear what we actually want here.

    }
}