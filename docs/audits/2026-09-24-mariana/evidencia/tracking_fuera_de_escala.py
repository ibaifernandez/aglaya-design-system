"""Letter-spacing en em escritos a mano que NO son ningún valor de la escala
--tracking-* del canon. Lee la escala en vivo de colors_and_type.css; no lleva
ningún valor dentro. Uso: python3 tracking_fuera_de_escala.py (desde la raíz del repo)."""
import re, subprocess, collections
css = re.sub(r"/\*[\s\S]*?\*/", "", open("colors_and_type.css", encoding="utf-8").read())
root = re.search(r":root\s*\{(.*?)\}", css, re.S).group(1)
tok = {v.strip() for n, v in re.findall(r"--([\w-]+)\s*:\s*([^;]+);", root) if n.startswith("tracking-")}
escala = {float(v[:-2]) if v.endswith("em") else 0.0 for v in tok}
ls = subprocess.run(["git", "ls-files", "ui_kits", "preview", "components", "colors_and_type.css"],
                    capture_output=True, text=True).stdout.split()
files = [f for f in ls if "/vendor/" not in f and f.endswith((".jsx", ".html", ".css", ".json"))]
pat = re.compile(r"""(?:letter-spacing|letterSpacing)["']?\s*[:=]\s*['"]?\s*(-?\d*\.?\d+em)""")
fuera = collections.defaultdict(list)
for f in files:
    for i, l in enumerate(open(f, encoding="utf-8").read().splitlines(), 1):
        for m in pat.finditer(l):
            if float(m.group(1)[:-2]) not in escala:
                fuera[m.group(1)].append(f"{f}:{i}")
tot = sum(len(v) for v in fuera.values())
fich = {x.split(":")[0] for v in fuera.values() for x in v}
print(f"escala del canon: {len(tok)} valores · fuera de escala: {tot} usos, {len(fuera)} valores distintos, en {len(fich)} ficheros")
for v, locs in sorted(fuera.items(), key=lambda x: -len(x[1])):
    print(f"  {len(locs):3d} x {v:>9}  {', '.join(locs)}")
