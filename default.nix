with (import <nixpkgs> {});
mkShell {
  buildInputs = with python312Packages; [
    openpyxl
    requests
    pyqt5
    beautifulsoup4
  ];
}