import json
import tempfile
from pathlib import Path

import streamlit as st

from modules.domain_intel import check_email_breach, resolve_dns, whois_lookup
from modules.metadata_extractor import extract_file_metadata
from modules.username_search import check_username

st.set_page_config(
    page_title="Ethical OSINT Toolkit",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        :root {
            --bg: #0b1020;
            --panel: #121a2b;
            --panel-2: #192235;
            --primary: #66d9ef;
            --success: #2dd4bf;
            --warning: #fbbf24;
            --danger: #f87171;
            --text: #e5ecff;
            --muted: #a6b3cf;
        }
        html, body, [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #0b1020 0%, #111827 100%);
            color: var(--text);
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
        }
        .stTabs [data-baseweb="tab"] {
            background: var(--panel-2);
            border-radius: 12px 12px 0 0;
            color: var(--text);
            padding: 0.75rem 1rem;
        }
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #0ea5e9, #22c55e);
            color: #08111d;
            font-weight: 700;
        }
        div[data-testid="stFileUploaderDropzone"] {
            border: 2px dashed rgba(102, 217, 239, 0.8);
            border-radius: 16px;
            background: rgba(18, 26, 43, 0.8);
        }
        .card {
            background: rgba(18, 26, 43, 0.85);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 16px;
            padding: 1rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.22);
        }
        .stAlert {
            border-radius: 12px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="card">
        <h2 style="margin-top: 0; color: #66d9ef;">🛡️ Ethical OSINT Toolkit</h2>
        <p style="color: #cfe0ff; margin-bottom: 0;">
            أداة احترافية للتحقيقات العامة والمرخصة فقط.
            تم تصميمها لاستخدامها لأغراض تعليمية أو مسموح بها فقط.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.warning(
    """
    هذا التطبيق مخصص فقط للاستخدام التعليمي أو المصرح به.
    لا تستخدمه في جمع بيانات غير مصرح بها أو البيانات الشخصية الخاصة.
    """
)

with st.sidebar:
    st.header("أدوات OSINT")
    st.caption("Mobile-friendly interface")
    st.markdown("---")
    st.markdown(
        """
        <div class="card">
            <strong>الإصدارات:</strong><br>
            • Username Enumeration<br>
            • Domain Intelligence<br>
            • Email Breach Lookup<br>
            • Metadata Extraction
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.caption("ملاحظات مهمة")
    st.info(
        "- بعض المنصات قد تمنع الطلبات الآلية.\n"
        "- بعض المعلومات قد تكون غير متاحة بشكل عام.\n"
        "- تعامل مع البيانات بمسؤولية ووفقاً للقوانين المطبقة."
    )

username_tab, domain_tab, email_tab, metadata_tab = st.tabs(
    ["Username", "Domain", "Email", "Metadata"]
)

with username_tab:
    st.subheader("ابحث عن اسم مستخدم")
    username = st.text_input("أدخل اسم المستخدم", placeholder="octocat")
    if st.button("بدء الفحص", use_container_width=True):
        if not username.strip():
            st.error("يرجى إدخال اسم مستخدم صحيح.")
        else:
            with st.spinner("جاري فحص اسم المستخدم عبر المنصات العامة..."):
                results = check_username(username, timeout=10)
            st.success("تم الانتهاء من الفحص")
            st.json(results)

with domain_tab:
    st.subheader("استطلاع النطاق")
    domain = st.text_input("أدخل النطاق", placeholder="github.com")
    if st.button("فحص النطاق", use_container_width=True):
        if not domain.strip():
            st.error("يرجى إدخال نطاق صالح.")
        else:
            with st.spinner("جاري جمع بيانات النطاق..."):
                dns_info = resolve_dns(domain)
                whois_info = whois_lookup(domain)
            st.success("تم جمع معلومات النطاق")
            st.json({"dns": dns_info, "whois": whois_info})

with email_tab:
    st.subheader("فحص تسريبات البريد الإلكتروني")
    email = st.text_input("أدخل البريد الإلكتروني", placeholder="someone@example.com")
    if st.button("بحث عن التسريبات", use_container_width=True):
        if not email.strip():
            st.error("يرجى إدخال بريد إلكتروني صحيح.")
        else:
            with st.spinner("جاري البحث في السجلات العامة للتسريبات..."):
                result = check_email_breach(email, timeout=10)
            st.success("تمت العملية")
            st.json(result)

with metadata_tab:
    st.subheader("استخراج البيانات الوصفية")
    uploaded_file = st.file_uploader(
        "تحميل صورة أو ملف PDF",
        type=["jpg", "jpeg", "png", "bmp", "gif", "tiff", "webp", "pdf"],
    )

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_path = temp_file.name

        with st.spinner("جاري استخراج البيانات الوصفية..."):
            result = extract_file_metadata(temp_path)

        st.success("تم استخراج البيانات الوصفية")
        st.json(result)

st.markdown("---")
st.caption("Built for authorized and educational OSINT use only.")
