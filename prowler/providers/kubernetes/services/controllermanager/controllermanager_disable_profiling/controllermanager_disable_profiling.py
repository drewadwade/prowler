from prowler.lib.check.models import Check, Check_Report_Kubernetes
from prowler.providers.kubernetes.services.controllermanager.controllermanager_client import (
    controllermanager_client,
)


class controllermanager_disable_profiling(Check):
    def execute(self) -> Check_Report_Kubernetes:
        findings = []
        for pod in controllermanager_client.controllermanager_pods:
            report = Check_Report_Kubernetes(metadata=self.metadata(), resource=pod)
            report.status = "PASS"
            report.status_extended = (
                f"Controller Manager does not have profiling enabled in pod {pod.name}."
            )
            for container in pod.containers.values():
                if "--profiling=false" not in str(container.command):
                    report.status = "FAIL"
                    report.status_extended = (
                        f"Controller Manager has profiling enabled in pod {pod.name}."
                    )
                    break
            findings.append(report)
        return findings
