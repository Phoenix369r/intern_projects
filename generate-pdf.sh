#!/bin/bash

# Resume PDF Generation Script
# This script demonstrates how to generate PDFs from the resume templates

echo "Resume PDF Generation Script"
echo "============================="

# Check if required tools are available
echo "Checking for required tools..."

# Check for wkhtmltopdf (HTML to PDF)
if command -v wkhtmltopdf &> /dev/null; then
    echo "✓ wkhtmltopdf found"
    HTML_TO_PDF=true
else
    echo "✗ wkhtmltopdf not found (install with: sudo apt-get install wkhtmltopdf)"
    HTML_TO_PDF=false
fi

# Check for pandoc (Markdown to PDF)
if command -v pandoc &> /dev/null; then
    echo "✓ pandoc found"
    PANDOC_AVAILABLE=true
else
    echo "✗ pandoc not found (install with: sudo apt-get install pandoc)"
    PANDOC_AVAILABLE=false
fi

# Check for pdflatex (LaTeX to PDF)
if command -v pdflatex &> /dev/null; then
    echo "✓ pdflatex found"
    LATEX_AVAILABLE=true
else
    echo "✗ pdflatex not found (install LaTeX distribution)"
    LATEX_AVAILABLE=false
fi

echo ""

# Generate PDFs if tools are available
if [ "$HTML_TO_PDF" = true ]; then
    echo "Generating PDF from HTML..."
    wkhtmltopdf --page-size A4 --orientation Portrait --margin-top 0.5in --margin-bottom 0.5in --margin-left 0.5in --margin-right 0.5in resume.html resume_from_html.pdf
    echo "✓ Generated: resume_from_html.pdf"
fi

if [ "$PANDOC_AVAILABLE" = true ]; then
    echo "Generating PDF from Markdown..."
    pandoc resume.md -o resume_from_markdown.pdf --pdf-engine=pdflatex
    echo "✓ Generated: resume_from_markdown.pdf"
fi

if [ "$LATEX_AVAILABLE" = true ]; then
    echo "Generating PDF from LaTeX..."
    pdflatex resume.tex
    # Run twice for proper references
    pdflatex resume.tex
    echo "✓ Generated: resume.pdf"
    
    # Clean up auxiliary files
    rm -f *.aux *.log *.out *.synctex.gz
fi

echo ""
echo "PDF generation complete!"
echo ""
echo "Manual generation instructions:"
echo "1. HTML to PDF: Use browser print function (Ctrl+P) and save as PDF"
echo "2. Markdown to PDF: Use online converters or Markdown editors with PDF export"
echo "3. LaTeX to PDF: Use Overleaf (overleaf.com) for online compilation"
echo ""
echo "Online tools:"
echo "- HTML to PDF: https://pdfshift.io/ or browser print function"
echo "- Markdown to PDF: https://md-to-pdf.fly.dev/"
echo "- LaTeX to PDF: https://overleaf.com/"