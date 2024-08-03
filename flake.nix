{
  description = "MindWM Python SDK";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/24.05";
    flake-parts.url = "github:hercules-ci/flake-parts";
    neomodel-py.url = "github:omgbebebe/neomodel.py-nix";
    neomodel-py.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = inputs@{ flake-parts, nixpkgs, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [];
      systems = [ "x86_64-linux" "aarch64-linux" ];
      perSystem = { config, self', inputs', pkgs, system, ... }:
      let
        my_python = pkgs.python3.withPackages (ps: with ps; [
          pydantic dateutil urllib3
          opentelemetry-sdk opentelemetry-exporter-otlp
          inputs.neomodel-py.packages.${system}.default
        ]);
        project = pkgs.callPackage ./package.nix {
          python = my_python;
        };
      in { 
        packages.default = project;
        devShells.default = pkgs.mkShell {
#          packages = [ project ];
          buildInputs = with pkgs; [
            my_python
            natscli
          ];
          shellHook = ''
            export PYTHONPATH="$PYTHONPATH:./src"
          '';
        };
      };
      flake = {
      };
    };
}
