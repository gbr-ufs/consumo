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
            packages = with pkgs; [
              file # For libmagic1.
              ffmpeg # For PyAV and yt-dlp.
              python312
              uv
            ];
          };
        }
      );
    };
}
