/etc/profile.d/java.sh:
  file.append:
    - text: export JAVA_HOME=/usr/lib/jvm/java-1.7.0

chmod -R a+w /tmp:
  cmd.run