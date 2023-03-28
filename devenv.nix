{ pkgs, ... }:

{
  # https://devenv.sh/basics/

  # https://devenv.sh/packages/
  packages = [ pkgs.git ];

  # https://devenv.sh/languages/
  languages.python.enable = true;
  languages.python.venv.enable = true;
}
