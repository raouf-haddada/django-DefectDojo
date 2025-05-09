import hashlib
import json
import re

from dojo.models import Finding


class MobsfscanParser:

    """A class that can be used to parse the mobsfscan (https://github.com/MobSF/mobsfscan) JSON report file."""

    SEVERITY = {
        "ERROR": "High",
        "WARNING": "Medium",
        "INFO": "Low",
    }

    def get_scan_types(self):
        return ["Mobsfscan Scan"]

    def get_label_for_scan_types(self, scan_type):
        return "Mobsfscan Scan"

    def get_description_for_scan_types(self, scan_type):
        return "Import JSON report for mobsfscan report file."

    def get_findings(self, filename, test):
        data = json.load(filename)
        if len(data.get("results")) == 0:
            return []
        dupes = {}
        for key, item in data.get("results").items():
            metadata = item.get("metadata")
            cwe = int(
                re.match(r"(cwe|CWE)-([0-9]+)", metadata.get("cwe")).group(
                    2,
                ),
            )
            masvs = metadata.get("masvs")
            owasp_mobile = metadata.get("owasp-mobile")
            description = "\n".join(
                [
                    f"**Description:** `{metadata.get('description')}`",
                    f"**OWASP MASVS:** `{masvs}`",
                    f"**OWASP Mobile:** `{owasp_mobile}`",
                ],
            )
            references = metadata.get("reference")
            severity = self.SEVERITY.get(metadata.get("severity"), "Info")

            files = []

            if item.get("files"):
                for file in item.get("files"):
                    file_path = file.get("file_path", "")
                    line = file.get("match_lines", [0])[0]
                    snippet = file.get("match_string", "")

                    files.append((file_path, line, snippet))
            else:
                files.append(("", 0, ""))

            for file_path, line, snippet in files:

                finding = Finding(
                    title=f"{key}",
                    test=test,
                    severity=severity,
                    nb_occurences=1,
                    cwe=cwe,
                    description=description,
                    references=references,
                )

                if file_path:
                    finding.file_path = file_path
                    finding.line = line
                    finding.description = f"{description}\n**Snippet:** `{snippet}`"

                dupe_key = hashlib.sha256(
                    (key + str(cwe) + masvs + owasp_mobile + file_path).encode("utf-8"),
                ).hexdigest()

                if dupe_key in dupes:
                    finding = dupes[dupe_key]
                    finding.nb_occurences += 1
                else:
                    dupes[dupe_key] = finding

        return list(dupes.values())
