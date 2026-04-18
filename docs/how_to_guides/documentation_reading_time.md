# Documentation Reading Time

consumo doesn't natively support directories. But this limitation can be surpassed by using standard Unix tools. Here's how to calculate the reading time of a repository's documentation by analyzing its Markdown files:

```shell
find . -name "*.md" -exec consumo file {} +
```
