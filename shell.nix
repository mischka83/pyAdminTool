{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = [
    (pkgs.python3.withPackages (pkgs: with pkgs; [
      pip
      numpy
      pandas
      requests
      cryptography
      flet
      flet-desktop
      flet-web
      pyinstaller
      pytest
      ldap3
    ]))
  ];
}