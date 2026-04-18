# Estimating the Reading Time of a Blog

consumo supports depth-based consumption time calculation through the `depth` option ("option" as in, command-line flag > configuration file > environment variable > project default). It is advised to also enable the `skip-errors` option, as you can't really know if a URL is alive or dead if you haven't visited it yet.

```shell
consumo url https://example.com/blog --depth 1 --skip-errors
```
