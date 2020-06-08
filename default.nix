let
  nixpkgs = builtins.fetchGit {
    name = "nixos-unstable-2020-05-9";
    url = "https://github.com/nixos/nixpkgs-channels/";
    ref = "refs/heads/nixos-unstable";
    rev = "46f975f81e0f71ba0d2b2bb8fe4006a9aa4c6c5c";
    # obtain via `git ls-remote https://github.com/nixos/nixpkgs-channels nixos-unstable`
  };
  pkgs = import nixpkgs { config = {}; };
  pythonCore = pkgs.python38;
  pythonPkgs = python-packages: with python-packages; [
      # TODO: figure out how to keep this out of the generate Docker container
      pytest

      sqlalchemy
      fastapi
      uvicorn
    ]; 
  myPython = pythonCore.withPackages pythonPkgs;
in
pkgs.mkShell {
  buildInputs =
  with pkgs;
  [
    sqlite
    git
    gnumake
    entr

    myPython
  ];
}
# TODO: add Docker support
