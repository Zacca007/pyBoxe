with (import <nixpkgs> {});
mkShell {
  buildInputs = with python312Packages; [
    openpyxl
    requests
    pyqt6
    beautifulsoup4
  ];
}
