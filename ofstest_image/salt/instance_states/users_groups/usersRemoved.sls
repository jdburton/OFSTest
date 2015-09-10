{% for user, args in pillar['usersRemoved'].iteritems() %}
{% if 'absent' in args %}
{{ user }}:
  user.absent:
    - gid: {{ args['gid'] }}
    - uid: {{ args['uid'] }}
    - force: {{ args['force'] }}
{% endif %}
{% endfor %}
