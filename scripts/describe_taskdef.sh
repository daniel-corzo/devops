aws ecs describe-task-definition --task-definition devops-fargate-task:2 \
    --query 'taskDefinition' \
    | jq 'del(.taskDefinitionArn, .revision, .status, .requiresAttributes, .compatibilities, .registeredAt, .deregisteredAt)' > taskdef.json
