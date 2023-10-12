{
  description = "Flake utils demo";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        overlays = [
        ];

        pkgs = import nixpkgs {
          inherit overlays system;
        };
      in
      {
        devShells = rec {
          default = empty;

          empty = pkgs.mkShell rec {
            buildInputs = with pkgs; [
              python3Packages.venvShellHook
            ];

            venvDir = ".venv";
            VENV_DIR = venvDir;
            PYTHONBREAKPOINT = "pudb.set_trace";
          };
        };
      }
    );
}
