{% load navigation_tags %}
{% load display_tags %}
{% url 'view_finding_group' finding_group.id as finding_group_url %}
{% url 'view_product' finding_group.test.engagement.product.id as product_url %}
{% url 'view_engagement' finding_group.test.engagement.id as engagement_url %}
{% url 'view_test' finding_group.test.id as test_url %}


*Findings Group*: [{{ finding_group.name|jiraencode}}|{{ finding_group_url|full_url }}] in [{{ finding_group.test.engagement.product.name|jiraencode }}|{{ product_url|full_url }}] / [{{ finding_group.test.engagement.name|jiraencode }}|{{ engagement_url|full_url }}] / [{{ finding_group.test|stringformat:'s'|jiraencode }}|{{ test_url|full_url }}]

*Severity:* {{ finding_group.severity }}

{% if finding_group|count_active > 0 %}
{% if finding_group|count_active > 50 %}
*findings:* First 50 of a total of {{ finding_group|count_active }} remaining active findings, ordered by severity.
{% else %}
*findings:* Total of {{ finding_group|count_active }} remaining active findings ordered by severity
{% endif %}
{% endif %}

|| Severity || CVE || Component || Version || Status ||{% for finding in finding_group.findings.all|slice:":50" %}{% if finding.active %}
| {{finding.severity}} | {% if finding.cve %}[{{finding.cve}}|{{finding.cve|vulnerability_url}}]{% elif finding.cve %}[{{finding.cwe}}|{{finding.cwe|cwe_url}}]{% endif %} | {{finding.component_name|jiraencode_component}} | {{finding.component_version}} | {{ finding.status }} |{% endif %}{% endfor %}{% for finding in finding_group.findings.all|slice:":50" %}{% if finding.is_mitigated and forloop.counter < finding_group|subtract %}
| {{finding.severity}} | {% if finding.cve %}[{{finding.cve}}|{{finding.cve|vulnerability_url}}]{% elif finding.cve %}[{{finding.cwe}}|{{finding.cwe|cwe_url}}]{% endif %} | {{finding.component_name|jiraencode_component}} | {{finding.component_version}} | {{ finding.status }} |{% endif %}{% endfor %}
