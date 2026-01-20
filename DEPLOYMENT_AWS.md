# Deploying Greeva Smart IoT to AWS

This guide outlines the steps to deploy the Greeva Hydroponics system to AWS using a modern containerized approach (AWS App Runner) which is the easiest and most cost-effective for this stack.

## 1. Prerequisites
- AWS Account
- Docker installed locally (for testing the build)
- AWS CLI configured

## 2. Infrastructure Setup (Recommended)
For a production-ready environment, you should use managed services:

1. **Database**: **Amazon RDS (MySQL)**
   - Create a MySQL instance.
   - Note the Endpoint, Username, and Password.
2. **Cache & Celery**: **Amazon ElastiCache (Redis)**
   - Create a Redis cluster.
   - Note the Primary Endpoint.
3. **Storage**: **Amazon S3**
   - Create a bucket for Static and Media files.
   - Ensure you have an IAM user with `AmazonS3FullAccess` to this bucket.

## 3. Deployment via AWS App Runner (Easiest)

### Step A: Push Image to Amazon ECR
1. Create a repository in ECR named `greeva-iot`.
2. Authenticate Docker to ECR:
   ```bash
   aws ecr get-login-password --region your-region | docker login --username AWS --password-stdin your-account-id.dkr.ecr.your-region.amazonaws.com
   ```
3. Build and Tag your image:
   ```bash
   docker build -t greeva-iot .
   docker tag greeva-iot:latest your-account-id.dkr.ecr.your-region.amazonaws.com/greeva-iot:latest
   ```
4. Push the image:
   ```bash
   docker push your-account-id.dkr.ecr.your-region.amazonaws.com/greeva-iot:latest
   ```

### Step B: Create App Runner Service
1. Go to **AWS App Runner** in the console.
2. Click **Create service**.
3. Source: **Container registry**, Provider: **Amazon ECR**.
4. Select your `greeva-iot` repository and tag.
5. In **Configuration**, add the following **Environment Variables**:

| Variable | Recommended Value |
|----------|-------------------|
| `DJANGO_SETTINGS_MODULE` | `config.settings.production` |
| `DJANGO_SECRET_KEY` | (Your random secret key) |
| `DJANGO_ALLOWED_HOSTS` | `*` (or your specific domain) |
| `DATABASE_URL` | `mysql://user:password@rds-endpoint:3306/dbname` |
| `REDIS_URL` | `redis://elasticache-endpoint:6379/0` |
| `DJANGO_AWS_ACCESS_KEY_ID` | (Your IAM Access Key) |
| `DJANGO_AWS_SECRET_ACCESS_KEY` | (Your IAM Secret Key) |
| `DJANGO_AWS_STORAGE_BUCKET_NAME` | (Your S3 Bucket Name) |
| `DJANGO_AWS_S3_REGION_NAME` | (e.g., `us-east-1`) |
| `DJANGO_ADMIN_URL` | (Custom admin path, e.g., `secret-admin/`) |
| `DATA_SOURCE` | `REAL` |

6. Set the **Port** to `8000`.
7. Review and Create.

## 4. Post-Deployment
Once the service is running:
1. **Migrations**: You can run migrations by temporarily changing the start command in App Runner to `python manage.py migrate --noinput` or by using a deployment script.
2. **Admin User**: Access the shell or use a script to create your first superuser on the RDS database.

## 5. Alternative: Elastic Beanstalk
If you prefer AWS Elastic Beanstalk (EB):
- Use the **Docker on Linux** platform.
- The `Dockerfile` provided in this repo will work out of the box.
- Configure environment variables in the EB console under Configuration > Software.
