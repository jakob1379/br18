{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    utils.url = "github:numtide/flake-utils";
  };
  outputs =
    {
      self,
      nixpkgs,
      utils,
    }:
    utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        formatter = pkgs.nixfmt-tree;

        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            uv
            crawley
            pandoc
            chromium
            single-file-cli
            ripgrep
            pv
            http-server
            lychee
            agent-browser
          ];

          shellHook = ''
            export CHROMIUM_PATH=${pkgs.chromium}/bin/chromium
            export UV_PYTHON_PREFERENCE="managed"
            export SSL_CERT_FILE=${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt
            export AGENT_BROWSER_EXECUTABLE_PATH=${pkgs.chromium}/bin/chromium
            unset LD_LIBRARY_PATH
          '';
        };
      }
    );

}
