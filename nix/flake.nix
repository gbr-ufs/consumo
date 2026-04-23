# SPDX-FileCopyrightText: 2026 Gabriel Santos de Souza <gabriel.santosdesouza@dcomp.ufs.br>
#
# SPDX-License-Identifier: GPL-3.0-or-later

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
            emacsSettings = pkgs.writeText "dir-locals.el" ''
              ((python-base-mode . ((apheleia-formatter . (ruff)))))
            '';
            neovimSettings = pkgs.writeText "nvim.lua" ''
              vim.lsp.config("ruff", {
                cmd = { "ruff", "server" }
                })
              vim.lsp.enable("ruff")
              vim.lsp.config("ty", {
                cmd = { "ty", "server" }
                })
              vim.lsp.enable("ty")
            '';
            VSCodeSettings = pkgs.writeText "settings.json" ''
              {
                "editor.formatOnSave": true,
                "python.defaultInterpreterPath": "''${workspaceFolder}/.venv/bin/python",
                "python.testing.pytestEnabled": true,
                "[python]": {
                  "editor.defaultFormatter": "charliermarsh.ruff"
                }
              }
            '';
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
                  rassumfrassum
                  uv
                ];
                shellHook = ''
                  mkdir -p .vscode
                  ln -sf ${emacsSettings} .dir-locals.el
                  ln -sf ${neovimSettings} .nvim.lua
                  ln -sf ${VSCodeSettings} .vscode/settings.json
                '';
              };
            }
        );
      };
}
