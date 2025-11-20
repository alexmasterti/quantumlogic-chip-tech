#!/usr/bin/env python3
"""
PDF Generator for QuantumLogic Chip Technology Technical Deep Dive

This script converts the technical_deep_dive.html presentation to a high-quality PDF
while preserving all styling, formatting, and professional appearance.
"""

import os
import sys
from pathlib import Path

# Add the virtual environment to Python path
venv_path = "/Users/alexcs/quantumlogic-chip-tech/demos/.venv/lib/python3.9/site-packages"
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

def generate_pdf():
    """Generate PDF from technical_deep_dive.html"""
    
    try:
        # Try to import weasyprint
        from weasyprint import HTML, CSS
        from weasyprint.text.fonts import FontConfiguration
    except ImportError:
        print("❌ WeasyPrint not found. Installing...")
        os.system("pip install weasyprint")
        try:
            from weasyprint import HTML, CSS
            from weasyprint.text.fonts import FontConfiguration
        except ImportError:
            print("❌ Failed to install WeasyPrint. Please install manually:")
            print("pip install weasyprint")
            return False
    
    # Set up paths
    current_dir = Path(__file__).parent
    html_file = current_dir / "presentations" / "technical_deep_dive.html"
    pdf_file = current_dir / "presentations" / "QuantumLogic_Technical_Deep_Dive.pdf"
    
    # Check if HTML file exists
    if not html_file.exists():
        print(f"❌ HTML file not found: {html_file}")
        return False
    
    print(f"🔄 Converting {html_file.name} to PDF...")
    
    # Additional CSS for better PDF rendering
    pdf_css = CSS(string="""
        @page {
            size: A4;
            margin: 0.5in;
            @bottom-center {
                content: "QuantumLogic Chip Technology - Technical Deep Dive";
                font-size: 10px;
                color: #666;
            }
            @bottom-right {
                content: "Page " counter(page);
                font-size: 10px;
                color: #666;
            }
        }
        
        body {
            background: white !important;
            font-size: 12px;
        }
        
        .container {
            box-shadow: none !important;
            margin: 0 !important;
            padding: 15px !important;
        }
        
        .header {
            margin: -15px -15px 30px -15px !important;
            page-break-inside: avoid;
        }
        
        .section {
            page-break-inside: avoid;
            margin: 30px 0 !important;
            padding: 20px !important;
        }
        
        .code-block {
            font-size: 9px !important;
            line-height: 1.3 !important;
            page-break-inside: avoid;
            overflow: visible !important;
        }
        
        .features-grid {
            display: grid !important;
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 15px !important;
        }
        
        .architecture-row {
            display: flex !important;
            gap: 10px !important;
        }
        
        .architecture-layer {
            flex: 1 !important;
            min-width: 0 !important;
            page-break-inside: avoid;
        }
        
        .metrics-table {
            font-size: 10px !important;
            page-break-inside: avoid;
        }
        
        .tech-stack {
            display: flex !important;
            flex-wrap: wrap !important;
            gap: 8px !important;
        }
        
        .tech-badge {
            font-size: 9px !important;
            padding: 6px 12px !important;
        }
        
        .conclusion {
            page-break-inside: avoid;
        }
        
        /* Ensure emojis render properly */
        .emoji {
            font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif;
        }
        
        /* Better page breaks */
        h2 {
            page-break-after: avoid;
        }
        
        h3 {
            page-break-after: avoid;
        }
        
        .highlight-box {
            page-break-inside: avoid;
        }
        
        .feature-card {
            page-break-inside: avoid;
        }
    """)
    
    try:
        # Create font configuration for better rendering
        font_config = FontConfiguration()
        
        # Convert HTML to PDF
        html_doc = HTML(filename=str(html_file))
        pdf_bytes = html_doc.write_pdf(
            stylesheets=[pdf_css],
            font_config=font_config,
            optimize_size=('fonts', 'images')
        )
        
        # Write PDF to file
        with open(pdf_file, 'wb') as f:
            f.write(pdf_bytes)
        
        print(f"✅ PDF generated successfully: {pdf_file}")
        print(f"📄 File size: {pdf_file.stat().st_size / (1024*1024):.1f} MB")
        
        return True
        
    except Exception as e:
        print(f"❌ Error generating PDF: {e}")
        return False

if __name__ == "__main__":
    print("🚀 QuantumLogic Technical Deep Dive PDF Generator")
    print("=" * 50)
    
    success = generate_pdf()
    
    if success:
        print("\n🎉 PDF generation completed successfully!")
        print("📂 The PDF is ready for distribution and presentations.")
    else:
        print("\n❌ PDF generation failed. Please check the error messages above.")
        sys.exit(1)
