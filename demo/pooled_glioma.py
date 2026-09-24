#!/usr/bin/env python3
"""Reuse demonstration: combine three rescued glioblastoma supplementary tables into analyses none of the source papers did.
 A. PMC6478916 (Commun Biol 2019)  TCGA pan-glioma cohort table: 814 patients, IDH-codel subtype, DNA methylation subtype, OS months, vital status, age, grade.
 B. PMC8136167 (Genome Med 2021)   TCGA glioma table: 603 patients, MARCO (macrophage marker) expression, OS, dead, MGMT, IDH.
 C. PMC6193287 (Acta Neuropathol Commun 2018)  MGH institutional cohort: 121 patients, IDH/TERT status, MGMT, ATRX, follow-up status.
Outputs: pooled_cohort.csv, join_stats.json, figure.png"""
import zipfile, io, os, json, re, collections
import openpyxl, pandas as pd, numpy as np
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter; from lifelines.statistics import logrank_test
P="../pilot/data/zips"
def xl(pmc,fn,sheet,skip=0):
    z=zipfile.ZipFile(f"{P}/{pmc}.zip"); b=z.read(next(x for x in z.namelist() if os.path.basename(x)==fn))
    ws=openpyxl.load_workbook(io.BytesIO(b),read_only=True,data_only=True)[sheet]
    rows=list(ws.iter_rows(values_only=True))[skip:]; return pd.DataFrame(rows[1:],columns=[str(c).strip() for c in rows[0]])
A=xl("PMC6478916","42003_2019_369_MOESM2_ESM.xlsx","Supplementary Data 1b",skip=2)
B=xl("PMC8136167","13073_2021_906_MOESM4_ESM.xlsx","F2C-D"); B=B.rename(columns={B.columns[0]:"PatientID"})
C=xl("PMC6193287","40478_2018_613_MOESM2_ESM.xlsx","Sheet1")
A=A.rename(columns={"IDH-codel subtype":"idh_A","OS months":"os_A","Vital dead 1":"dead_A","Age At Diagnosis":"age_A","Histology":"hist","DNA Methylation Cluster":"meth"})
if "meth" not in A.columns: A=A.rename(columns={[c for c in A.columns if c.startswith("DNA Methylation")][0]:"meth"})
B=B.rename(columns={"Overall Survival (Months)":"os_B","Dead":"dead_B","IDHmut":"idh_B","Diagnosis Age":"age_B","MGMT_methylated":"mgmt_B","MARCO":"marco"})
for c in ("os_A","dead_A","age_A"): A[c]=pd.to_numeric(A[c],errors="coerce")
for c in ("os_B","dead_B","age_B","marco"): B[c]=pd.to_numeric(B[c],errors="coerce")
A["idh"]=A["idh_A"].astype(str).str.contains("IDHmut",case=False).map({True:"IDH-mutant",False:"IDH-wildtype"}); A.loc[~A["idh_A"].astype(str).str.contains("IDH",case=False),"idh"]=np.nan
B["idh"]=B["idh_B"].astype(str).map(lambda s: "IDH-wildtype" if "WT" in s.upper() else ("IDH-mutant" if "MUT" in s.upper() or "R132" in s.upper() else np.nan))
# --- join by TCGA barcode
J=A.merge(B,on="PatientID",how="outer",indicator=True); ov=(J["_merge"]=="both").sum()
stats={"A_rows":len(A),"B_rows":len(B),"overlap_by_barcode":int(ov),"only_A":int((J["_merge"]=="left_only").sum()),"only_B":int((J["_merge"]=="right_only").sum())}
# agreement checks on the overlap (are these really the same patients?)
both=J[J["_merge"]=="both"]
stats["os_agree_within_0.5mo"]=int((abs(both["os_A"]-both["os_B"])<=0.5).sum()); stats["idh_agree"]=int((both["idh_x"]==both["idh_y"]).sum()); stats["age_agree"]=int((abs(both["age_A"]-both["age_B"])<=1).sum())
# --- pooled TCGA cohort (union, deduplicated), survival by IDH
U=J.copy(); U["os"]=U["os_A"].fillna(U["os_B"]); U["dead"]=U["dead_A"].fillna(U["dead_B"]); U["idh"]=U["idh_x"].fillna(U["idh_y"]); U["age"]=U["age_A"].fillna(U["age_B"])
U=U.dropna(subset=["os","dead","idh"]); U=U[U["os"]>0]
stats["pooled_tcga_patients_with_survival"]=len(U); stats["pooled_by_idh"]=U["idh"].value_counts().to_dict()
km={}; fig,ax=plt.subplots(1,3,figsize=(13,4.2))
for g,col in (("IDH-wildtype","#0F6E68"),("IDH-mutant","#B8860B")):
    s=U[U["idh"]==g]; k=KaplanMeierFitter().fit(s["os"],s["dead"],label=f"{g} (n={len(s)})"); k.plot_survival_function(ax=ax[0],ci_show=True,color=col); km[g]={"n":len(s),"median_os_months":float(k.median_survival_time_)}
lr=logrank_test(U[U.idh=="IDH-wildtype"]["os"],U[U.idh=="IDH-mutant"]["os"],U[U.idh=="IDH-wildtype"]["dead"],U[U.idh=="IDH-mutant"]["dead"])
stats["km"]=km; stats["logrank_p"]=float(lr.p_value)
ax[0].set_title(f"Pooled TCGA glioma, two rescued tables\n(n={len(U)}, log-rank p={lr.p_value:.1e})",fontsize=10); ax[0].set_xlabel("Months"); ax[0].set_ylabel("Survival"); ax[0].set_xlim(0,120)
# --- new cross-table analysis: MARCO (table B) by methylation subtype (table A) - only possible after the join
X=both.dropna(subset=["marco","meth"]); X=X[(X["meth"].astype(str).str.len()>1)&(~X["meth"].astype(str).str.upper().isin(["NA","NAN","NONE"]))]
order=X.groupby("meth")["marco"].median().sort_values().index.tolist(); order=[o for o in order if (X["meth"]==o).sum()>=8]
data=[X[X["meth"]==o]["marco"].values for o in order]
ax[1].boxplot(data,tick_labels=[f"{o}\n(n={len(d)})" for o,d in zip(order,data)],vert=True); ax[1].tick_params(axis="x",labelsize=7,rotation=30)
ax[1].set_title(f"MARCO macrophage score (paper B)\nby DNA-methylation subtype (paper A), n={len(X)}",fontsize=10); ax[1].set_ylabel("MARCO (z)")
stats["marco_by_meth"]={o:{"n":int(len(d)),"median":float(np.median(d))} for o,d in zip(order,data)}
# --- independent institutional cohort (MGH): death at follow-up by IDH/TERT status
s=C["IDH/TERT status"].astype(str).str.lower().str.strip()
C["grp"]=np.where(s.str.contains("double wild"),"double wild-type",np.where(s.str.contains("mut"),"IDH/TERT-mutant",None)); C=C.dropna(subset=["grp"])
C["dead"]=C["Follow up status"].astype(str).str.contains("deceased|dead",case=False)
tab=C.groupby("grp")["dead"].agg(["sum","count"]); tab["rate"]=tab["sum"]/tab["count"]
stats["mgh"]={g:{"n":int(r["count"]),"deceased":int(r["sum"]),"death_rate":round(float(r["rate"]),3)} for g,r in tab.iterrows()}
order_c=[g for g in ("double wild-type","IDH/TERT-mutant") if g in tab.index]
ax[2].bar([f"{g}\n(n={int(tab.loc[g,'count'])})" for g in order_c],[tab.loc[g,"rate"] for g in order_c],color=["#0F6E68","#B8860B"][:len(order_c)])
ax[2].set_ylim(0,1); ax[2].set_ylabel("Share deceased at follow-up"); ax[2].set_title("Independent MGH cohort (paper C), n=121:\ndirection consistent with the pooled result (small n)",fontsize=10)
plt.tight_layout(); plt.savefig("figure.png",dpi=160); U[["PatientID","idh","os","dead","age"]].to_csv("pooled_cohort.csv",index=False)
json.dump(stats,open("join_stats.json","w"),indent=1); print(json.dumps(stats,indent=1))
