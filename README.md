# Terragrunt Plan Explainer

This GitHub Action explains Terragrunt plans using Google AI and posts the explanation as a comment on the pull request.

## Inputs

- `GOOGLE_API_KEY`: Google AI API Key (required)
- `GITHUB_TOKEN`: GitHub token for API access (required)
- `TF_PLAN`: Terragrunt plan output (required)

## Example usage
```yaml
name: Terragrunt Plan and Explain
on: [pull_request]

jobs:
  plan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      # Add steps to set up Terragrunt and run the plan
      - name: Terragrunt plan
        id: terragrunt_plan
        run: |
          # Your Terragrunt plan command here
          terragrunt plan -out=tfplan.out
          terragrunt show -no-color tfplan.out > tfplan.txt
      
      - name: Explain Terragrunt plan
        uses: speakmanra/terragrunt-plan-explainer@v1
        with:
          GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          TF_PLAN: ${{ steps.terragrunt_plan.outputs.plan }}
```