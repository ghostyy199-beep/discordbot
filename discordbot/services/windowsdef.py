import subprocess


class WindowsDefender:
    @staticmethod
    def _run_powershell(command: str) -> str:
        result = subprocess.run(
            ["powershell", "-Command", command],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr)

        return result.stdout.strip()

    @classmethod
    def is_realtime_enabled(cls) -> bool:
        command = "Get-MpComputerStatus | Select-Object -ExpandProperty RealTimeProtectionEnabled"
        status = cls._run_powershell(command)
        return status.lower() == "true"

    @classmethod
    def disable_realtime(cls):
        command = "Set-MpPreference -DisableRealtimeMonitoring $true"
        cls._run_powershell(command)