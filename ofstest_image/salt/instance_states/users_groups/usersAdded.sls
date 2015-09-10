{% for user, args in pillar['usersAdded'].iteritems() %}
{% if 'present' in args %}
{{ user }}:
  group.present:
    - gid: {{ args['gid'] }}
  user.present:
    - gid: {{ args['gid'] }}
    - uid: {{ args['uid'] }}
    - fullname: {{ args['fullname'] }}
    - shell: {{ args['shell'] }}
    - home: {{ args['home'] }}
    - password: {{ args['password'] }}
{% if 'groups' in args %}
    - groups: {{ args['groups'] }}
    - require:
      - group: {{ user }} 
{% endif %}
{% endif %}
{% endfor %}
