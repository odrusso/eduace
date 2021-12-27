import {expect as expectCDK, matchTemplate, MatchStyle, haveResource} from '@aws-cdk/assert';
import * as cdk from '@aws-cdk/core';
import * as Infra from '../lib/eduace-web-app';

test('Smoke test', () => {
    const app = new cdk.App();
    const mockEnv = {account: "1234", region: "ap-southeast-2"}
    const stack = new Infra.EduaceWebApp(app, 'MyTestStack', {env: mockEnv});
    // We want to make sure that we're synthesising something
    expectCDK(stack).to(haveResource("AWS::S3::Bucket"))
    expectCDK(stack).to(haveResource("AWS::CloudFront::Distribution"))
    expectCDK(stack).notTo(haveResource("AWS::ApiGateway::Method"))
});
