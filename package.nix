{ lib
, pkgs
, python
}:
with pkgs;

python3.pkgs.buildPythonPackage {
  pname = "mindwm-sdk-python";
  version = "0.1.0";

  src = ./.;

  propagatedBuildInputs = [ python dbus ];

  format = "pyproject";
  nativeBuildInputs = with python3.pkgs; [ setuptools ];
}
