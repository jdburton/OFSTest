# Workaround for a bug where dnf returns failure on certain warnings.
dnf clean all && dnf update -y --disableexcludes=main || true:
  cmd.run

