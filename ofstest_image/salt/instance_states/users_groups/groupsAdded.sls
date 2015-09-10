{% for group, args in pillar['groupsAdded'].iteritems() %}
{% if 'present' in args %}
{{ group }}:
  group.present:
    - name: {{ group }}
    - gid: {{ args['gid'] }}
{% endif %}
{% endfor %}
