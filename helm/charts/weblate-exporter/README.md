# weblate-exporter

![Version: 1.1.2](https://img.shields.io/badge/Version-1.1.2-informational?style=flat-square) ![Type: application](https://img.shields.io/badge/Type-application-informational?style=flat-square) ![AppVersion: v1.1.2](https://img.shields.io/badge/AppVersion-v1.1.2-informational?style=flat-square)

Weblate prometheus metrics exporter

## TL;DR;

```console
$ helm repo add weblate-exporter https://raw.githubusercontent.com/loktionovam/weblate_exporter/gh-pages/
$ helm repo update

$ helm search repo --versions weblate-exporter

 NAME                             	CHART VERSION	APP VERSION	DESCRIPTION
 weblate-exporter/weblate-exporter	0.3.2        	v0.3.2     	Weblate prometheus metrics exporter

$  helm install weblate-exporter weblate-exporter/weblate-exporter \
    --version 0.3.2 \
    --set config.weblateAPIUrl="http://weblate.example.com:8080/api/" \
    --set config.weblateAPIKey="secret_api_key"

$ helm test weblate-exporter
```

## Values

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| affinity | object | `{}` |  |
| config.weblateAPIKey | string | `""` | weblate API key, which you can get in your profile |
| config.weblateAPIUrl | string | `""` | weblate API URL, i.e http://weblate.example.com/api/ Note: The trailing slash in URL is mandatory |
| config.weblateExporterPort | int | `9867` | weblate exporter bind port |
| fullnameOverride | string | `""` |  |
| image.pullPolicy | string | `"IfNotPresent"` |  |
| image.repository | string | `"loktionovam/weblate_exporter"` |  |
| image.tag | string | `"v1.1.2"` |  |
| imagePullSecrets | list | `[]` |  |
| ingress.annotations | object | `{}` |  |
| ingress.className | string | `""` |  |
| ingress.enabled | bool | `false` |  |
| ingress.hosts[0].host | string | `"weblate-exporter.local"` |  |
| ingress.hosts[0].paths[0].path | string | `"/"` |  |
| ingress.hosts[0].paths[0].pathType | string | `"ImplementationSpecific"` |  |
| ingress.tls | list | `[]` |  |
| nameOverride | string | `""` |  |
| nodeSelector | object | `{}` |  |
| podAnnotations | object | `{}` |  |
| podSecurityContext | object | `{}` |  |
| replicaCount | int | `1` |  |
| resources.limits.cpu | string | `"100m"` |  |
| resources.limits.memory | string | `"64Mi"` |  |
| resources.requests.cpu | string | `"100m"` |  |
| resources.requests.memory | string | `"64Mi"` |  |
| securityContext.readOnlyRootFilesystem | bool | `true` |  |
| securityContext.runAsNonRoot | bool | `true` |  |
| securityContext.runAsUser | int | `1000` |  |
| service.port | int | `9867` |  |
| service.type | string | `"ClusterIP"` |  |
| serviceAccount.annotations | object | `{}` | Annotations to add to the service account |
| serviceAccount.create | bool | `true` | Specifies whether a service account should be created |
| serviceAccount.name | string | `""` | The name of the service account to use. If not set and create is true, a name is generated using the fullname template |
| serviceMonitor.enabled | bool | `true` |  |
| serviceMonitor.interval | string | `"1m"` |  |
| serviceMonitor.port | string | `"http"` |  |
| tolerations | list | `[]` |  |
