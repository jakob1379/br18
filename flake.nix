{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, utils }: utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
    in
      {
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
          ];

          LD_LIBRARY_PATH = "${pkgs.lib.makeLibraryPath (with pkgs; [ xorg.libX11 ])
                              }:$LD_LIBRARY_PATH";
          shellHook = ''
            export CHROMIUM_PATH=${pkgs.chromium}/bin/chromium
            export UV_PYTHON_PREFERENCE="managed"
            export SSL_CERT_FILE=${pkgs.cacert}/etc/ssl/certs/ca-bundle.crt
            '';
        };
      }
  );

}
