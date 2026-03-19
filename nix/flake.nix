{
  description = "Content consumption analyzer CLI.";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/master";
  };
  outputs =
    { nixpkgs, ... }:
    let
      inherit (nixpkgs) lib;
      forAllSystems = lib.genAttrs lib.systems.flakeExposed;
    in
    {
      devShells = forAllSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          default = pkgs.mkShell {
            LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib:${
              pkgs.lib.makeLibraryPath [
                pkgs.ffmpeg
                pkgs.file
              ]
            }:$LD_LIBRARY_PATH";
            packages = with pkgs; [
              ffmpeg # For PyAV and yt-dlp.
              file # For libmagic1.
              python312
              uv
            ];
          };
        }
      );
    };
}
