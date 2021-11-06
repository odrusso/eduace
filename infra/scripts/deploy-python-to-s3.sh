# Usage sh update.sh [app-name]

# Create package bundle
zip -r build.zip ../app/build/build.py

# Redeploy to AWS
aws s3 cp build.zip s3://infrastack-eduacebackendeduacebackendlambdastore1-1hbxoz5m08h6l/build.zip

# Clean-up
rm -f build.zip
