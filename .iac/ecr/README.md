<br>

## Notes

### Creating an Amazon Elastic Container Registry Repository

The script [registry.sh.template](registry.sh.template) outlines the [creation of an Amazon ECR (Elastic Container Registry) repository](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ecr/create-repository.html).  Always ensure the _**tags text**_, study [registry.json](registry.json), does not include special characters.

```shell
bash .iac/ecr/registry.sh
```

If successful, the terminal output pattern is

```json
{
    "repository": {
        "repositoryArn": "arn:aws:ecr:{region.code}:{account.identifier}:repository/{repository.name}",
        "registryId": "{account.identifier}",
        "repositoryName": "{repository.name}",
        "repositoryUri": "{account.identifier}.dkr.ecr.{region.code}.amazonaws.com/{repository.name}",
        "createdAt": "2024-09-08T02:37:57.880000+01:00",
        "imageTagMutability": "MUTABLE",
        "imageScanningConfiguration": {
            "scanOnPush": false
        },
        "encryptionConfiguration": {
            "encryptionType": "{encryption.type}"
        }
    }
}
```

Ensure the GitHub Action of this GitHub repository can extract the name of the created ECR repository via GitHub Secrets.

| GitHub Secret<br>Identifier | Notes                                                                                               |
|:----------------------------|:----------------------------------------------------------------------------------------------------|
| AWS_ECR_REPOSITORY_SANDBOX  | Provides the name of the Amazon ECR repository that this repository's image should be delivered to. |


<br>
<br>


### Deleting


Repository [deletion](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/ecr/delete-repository.html):

```shell
aws ecr delete-repository \
    --repository-name {repository.name} \
    --force
```



<br>
<br>

<br>
<br>

<br>
<br>

<br>
<br>
