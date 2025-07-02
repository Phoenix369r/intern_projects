# Intern Projects

This repository contains various projects developed during internship programs, including a modern professional resume template.

## 📄 Professional Resume Template

A comprehensive, modern resume template available in multiple formats designed for professional use and ATS compatibility.

### 🎯 Features

- **Multiple Formats**: HTML, Markdown, and LaTeX versions
- **Responsive Design**: Works on all screen sizes
- **ATS-Friendly**: Compatible with Applicant Tracking Systems
- **Professional Styling**: Clean, modern design with subtle colors
- **Print Optimized**: Looks great when printed
- **Easy Customization**: Well-documented and easy to modify

### 📁 Resume Files

| File | Description | Use Case |
|------|-------------|----------|
| `resume.html` | HTML version with embedded CSS | Web viewing, online portfolios |
| `resume.css` | Separate stylesheet | Modular styling, customization |
| `resume.md` | Markdown version | Easy editing, GitHub profiles |
| `resume.tex` | LaTeX template | Professional PDF generation |

### 🚀 Quick Start

#### HTML Resume
1. Open `resume.html` in any web browser
2. Edit the content directly in the HTML file
3. Customize styling in `resume.css` if needed

#### Markdown Resume
1. Edit `resume.md` in any text editor
2. Use Markdown preview in GitHub, VS Code, or similar
3. Convert to PDF using tools like Pandoc if needed

#### LaTeX Resume
1. Install LaTeX distribution (TeX Live, MiKTeX, or MacTeX)
2. Install moderncv package: `tlmgr install moderncv`
3. Compile: `pdflatex resume.tex`
4. Alternative: Use [Overleaf](https://overleaf.com) online

### ✏️ Customization Guide

#### Personal Information
- Replace placeholder text with your actual information
- Update contact details, social media links
- Modify professional title and summary

#### Content Sections
- **Professional Summary**: Tailor to your experience
- **Education**: Add your academic background
- **Technical Skills**: Update with your technologies
- **Work Experience**: Include your work history
- **Projects**: Showcase your best work
- **Certifications**: List relevant certifications

#### Styling (HTML/CSS)
```css
/* Change color scheme */
.header {
    background: linear-gradient(135deg, #your-color1, #your-color2);
}

/* Modify accent colors */
.section-title {
    border-bottom-color: #your-accent-color;
}
```

#### Theme Options
- **Default**: Blue gradient theme
- **Green**: Add `theme-green` class to container
- **Purple**: Add `theme-purple` class to container
- **ATS-Friendly**: Add `ats-friendly` class to container

### 🎨 Color Schemes

| Theme | Primary | Secondary | Use |
|-------|---------|-----------|-----|
| Default | #2c3e50 | #3498db | Professional, tech |
| Green | #27ae60 | #2ecc71 | Healthcare, environment |
| Purple | #8e44ad | #9b59b6 | Creative, design |

### 📱 Responsive Breakpoints

- **Desktop**: > 768px (full layout)
- **Tablet**: 481px - 768px (adjusted spacing)
- **Mobile**: ≤ 480px (single column, compressed)

### 🖨️ Print Optimization

The resume is optimized for printing with:
- Proper page breaks
- Print-friendly colors
- Optimized font sizes
- Clean layout without shadows

### ♿ Accessibility Features

- High contrast mode support
- Reduced motion preferences
- Semantic HTML structure
- Screen reader friendly

### 📋 ATS Compatibility Tips

1. Use standard section headings
2. Include keywords from job descriptions
3. Use simple formatting
4. Avoid tables and complex layouts
5. Save as .txt for some systems

### 🛠️ Development Tools

#### Required for LaTeX
- LaTeX distribution (TeX Live recommended)
- moderncv package
- Basic LaTeX editor or Overleaf

#### Optional Tools
- **Pandoc**: Convert between formats
- **wkhtmltopdf**: HTML to PDF conversion
- **VS Code**: LaTeX Workshop extension

### 📝 Content Guidelines

#### Professional Summary
- 3-4 sentences maximum
- Include years of experience
- Mention key technologies/skills
- Quantify achievements when possible

#### Work Experience
- Use action verbs (developed, implemented, led)
- Include quantifiable results (improved by 30%)
- Focus on achievements, not just duties
- Keep bullet points concise

#### Technical Skills
- Group by category
- List most relevant skills first
- Include proficiency levels if appropriate
- Update based on job requirements

### 🔄 Version Control

Track your resume changes:
```bash
# Initialize git in your resume folder
git init
git add .
git commit -m "Initial resume version"

# Create branches for different job applications
git checkout -b company-specific-version
```

### 📤 Export Options

#### PDF Generation
- **HTML to PDF**: Use browser print function or wkhtmltopdf
- **Markdown to PDF**: Use Pandoc with LaTeX
- **LaTeX to PDF**: Use pdflatex compiler

#### Word Document
- Convert HTML using online converters
- Use Pandoc: `pandoc resume.md -o resume.docx`

### 🎯 Job Application Tips

1. **Tailor for each job**: Adjust keywords and skills
2. **File naming**: Use format "FirstName_LastName_Resume.pdf"
3. **Multiple versions**: Keep different versions for different roles
4. **Regular updates**: Update every 3-6 months
5. **Backup**: Keep copies in cloud storage

## 🔧 Other Projects

- **Google Translator 2.0**: Python-based translation application using tkinter and Google Translate API

## 📞 Support

For questions or issues with the resume template:
1. Check the customization guide above
2. Review the comments in the source files
3. Create an issue in this repository

---

*Professional resume template designed for modern job applications. Customize according to your needs and industry requirements.*
