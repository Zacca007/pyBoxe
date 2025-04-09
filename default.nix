with (import <nixpkgs> {});
mkShell {
  buildInputs = with python312Packages; [
    openpyxl
    requests
    beautifulsoup4
    pyqt6
    tkinter
  ];
}
