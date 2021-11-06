#!/usr/bin/env node
import 'source-map-support/register';
import {EduaceWebApp} from '../lib/eduace-web-app';
import {App} from "@aws-cdk/core";

const app = new App();
new EduaceWebApp(app, 'InfraStack', {
  env: {
    account: process.env.CDK_DEFAULT_ACCOUNT,
    region: process.env.CDK_DEFAULT_REGION
  },
});
