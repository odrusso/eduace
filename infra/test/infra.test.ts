import {expect as expectCDK, matchTemplate, MatchStyle, haveResource} from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as Infra from '../lib/eduace-web-app';

test('Smoke test', () => {
    const app = new cdk.App();
    const stack = new Infra.EduaceWebApp(app, 'MyTestStack');
    // We want to make sure that we're synthesising something
    expectCDK(stack).to(haveResource("AWS::S3::Bucket"))
    expectCDK(stack).to(haveResource("AWS::ApiGateway::Method"))
    expectCDK(stack).to(haveResource("AWS::Lambda::Function"))
});
