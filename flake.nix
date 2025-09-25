{
  description = "A development shell for a Python project";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  };
  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          (python312.withPackages (ps: with ps; [
            # List your Python packages here
            scipy
            numpy
            matplotlib
            /*(matplotlib.override{
              enableGtk3 = true;
            })
            # For example: numpy, pandas, etc.
            (pkgs.qemu_full.override { 
              enableDocs = false; 
              cephSupport = false; 
            })*/
          ]))
        ];
      };
    };
}