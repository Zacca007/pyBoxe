with (import <nixpkgs> {});
mkShell {
  buildInputs = with python313Packages; [
    openpyxl
    requests
    beautifulsoup4
    pyqt6
    tkinter

    libreoffice
  ];
}
