{% for group, args in pillar['groupsRemoved'].iteritems() %}
{% if 'absent' in args %}
{{ group }}:
  group.absent:
    - name: {{ group }}
    - gid: {{ args['gid'] }}
{% endif %}
{% endfor %}
