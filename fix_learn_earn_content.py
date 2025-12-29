import re
from home.models import Pages

def clean_learn_and_earn():
    try:
        p = Pages.objects.get(slug='learn-and-earn')
        desc = p.description
        print("Original description length:", len(desc))

        # --- Fix 1: Ordered Lists (Numbered Paragraphs) ---
        # Pattern matches sequences of: <p><span ...>NUMBER. &nbsp;CONTENT</span></p>
        # We capture the style, the number (ignored), and the content.
        
        # Regex explanation:
        # (?: ... ){2,} : Match 2 or more occurrences of the paragraph pattern
        # <p>(<span[^>]*>)\s*\d+\.\s*&nbsp;(.*?)</span></p> : Match individual item
        
        pattern_ol = r'(?:<p><span[^>]*>\s*\d+\.\s*&nbsp;.*?</span></p>\s*){2,}'
        
        def ol_converter(match):
            block = match.group(0)
            # Extract individual items from the matched block
            lines = re.findall(r'<p>(<span[^>]*>)\s*\d+\.\s*&nbsp;(.*?)</span></p>', block)
            if not lines:
                return block
                
            items = []
            for style_tag, content in lines:
                # Reconstruct as LI. usage of style_tag preserves color/font
                items.append(f'    <li>{style_tag}{content}</span></li>')
            
            return '<ol>\n' + '\n'.join(items) + '\n</ol>'

        new_desc = re.sub(pattern_ol, ol_converter, desc, flags=re.DOTALL)

        # --- Fix 2: Bullet List (Embedded in P) ---
        # The specific messy block about volatility.
        # We target a recognizable substring and replace the whole chunk with clean HTML.
        
        messy_start = "There are a few possible causes of volatility listed below:<br />"
        messy_end = "Interesting Read: How to handle volatility in the markets?</span></p>"
        
        # We construct a regex that captures everything between start and end within that P tag
        # The structure is: <p><span ...>...messy_start ... messy_end
        
        # Since matching the exact HTML string (with all nested tags/newlines) is fragile,
        # we will use a simpler replace for the bullet lines if we can find them.
        
        # Let's match the specific content block we saw in the verification step.
        # "&bull; Aspects related to politics and economy<br />"
        
        # Replacement map for the bullet section
        if "&bull; Aspects related to politics and economy" in new_desc:
             print("Found bullet section")
             
             # Locate the <p> containing this.
             # It's difficult to replace just the P because valid HTML depends on closing tags.
             # We will try to replace the content string literal.
             
             # The target string segment (simplified based on output):
             target_segment = """&bull; Aspects related to politics and economy<br />
<br />
&bull; Sector and industry-specific factors.<br />
<br />
&bull; The company&#39;s performance.<br />"""

             replacement_segment = """</ul>
<ul>
    <li>Aspects related to politics and economy</li>
    <li>Sector and industry-specific factors.</li>
    <li>The company&#39;s performance.</li>
</ul>
<p>""" 
             # Note: The above replacement is a hack to close/open tags, but it assumes context.
             # A safer way is to replace the known entities with <li> and trust the browser or style it.
             
             # Let's try a safer full-block replacement if we can identify the context.
             # We seek:
             # <p><span...> ... causes of volatility listed below:<br /> ... &bull; ... </span></p>
             
             # Find the whole Paragraph containing "causes of volatility"
             p_pattern = r'<p><span[^>]*>.*?causes of volatility listed below:.*?</span></p>'
             match = re.search(p_pattern, new_desc, re.DOTALL)
             if match:
                 original_p = match.group(0)
                 # Now clean this specific P
                 # 1. Split into proper blocks
                 # 2. Extract span style
                 span_match = re.search(r'<span([^>]*)>', original_p)
                 style_attr = span_match.group(1) if span_match else ' style="color:#000000;"'
                 
                 clean_html = f"""<p><span{style_attr}>Conversely, if &beta; = 0.8 is present in the stock, it means that for every 100% movement in the benchmark or underlying index, the stock has moved 80%.</span></p>

<p><span{style_attr}>The volatility index, or VIX, can also be used to measure market volatility. Option contracts are priced using other techniques such as binomial tree models or Black-Scholes models.</span></p>

<p><span{style_attr}>There are a few possible causes of volatility listed below:</span></p>

<ul>
    <li><span{style_attr}>Aspects related to politics and economy</span></li>
    <li><span{style_attr}>Sector and industry-specific factors.</span></li>
    <li><span{style_attr}>The company&#39;s performance.</span></li>
</ul>

<p><span{style_attr}>Interesting Read: How to handle volatility in the markets?</span></p>"""

                 # Only replace if the match covered the whole messy block. 
                 # The regex `.*?` is greedy within the P. 
                 # Let's verification: The P started way back at "Conversely..."
                 
                 if "Conversely" in original_p:
                     new_desc = new_desc.replace(original_p, clean_html)
                     print("Replaced messy bullet paragraph.")
        
        # Save changes
        if new_desc != desc:
            p.description = new_desc
            p.save()
            print("Successfully updated description.")
        else:
            print("No changes made (patterns not found?)")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    clean_learn_and_earn()
