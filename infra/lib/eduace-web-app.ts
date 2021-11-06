import {EduaceBackend} from "./eduace-backend";
import {Construct, Stack, StackProps} from "@aws-cdk/core";

export class EduaceWebApp extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    new EduaceBackend(this, "EduaceBackend")
  }
}
