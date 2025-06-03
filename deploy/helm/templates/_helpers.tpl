{{/*
Expand the name of the chart.
*/}}
{{- define "kvcache-api-layer.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "kvcache-api-layer.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "kvcache-api-layer.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "kvcache-api-layer.labels" -}}
helm.sh/chart: {{ include "kvcache-api-layer.chart" . }}
{{ include "kvcache-api-layer.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- with .Values.commonLabels }}
{{ toYaml . }}
{{- end }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "kvcache-api-layer.selectorLabels" -}}
app.kubernetes.io/name: {{ include "kvcache-api-layer.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Common annotations
*/}}
{{- define "kvcache-api-layer.annotations" -}}
{{- with .Values.commonAnnotations }}
{{ toYaml . }}
{{- end }}
{{- end }}

{{/*
Generate node IP mapping environment variables
*/}}
{{- define "kvcache-api-layer.nodeIPEnv" -}}
{{- if .Values.nodeIPMapping }}
{{- range $nodeName, $nodeIP := .Values.nodeIPMapping }}
- name: NODE_IP_{{ $nodeName | upper | replace "-" "_" | replace "." "_" }}
  value: {{ $nodeIP | quote }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Generate script to resolve node IP from mapping or use detected IP
*/}}
{{- define "kvcache-api-layer.resolveNodeIP" -}}
# 解析节点IP
RESOLVED_NODE_IP="$NODE_IP"
{{- if .Values.nodeIPMapping }}
{{- range $nodeName, $nodeIP := .Values.nodeIPMapping }}
if [ "$NODE_NAME" = "{{ $nodeName }}" ]; then
  RESOLVED_NODE_IP="{{ $nodeIP }}"
fi
{{- end }}
{{- end }}
export RESOLVED_NODE_IP="$RESOLVED_NODE_IP"
echo "Node: $NODE_NAME, Resolved IP: $RESOLVED_NODE_IP"
{{- end }} 