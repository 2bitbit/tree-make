from config import sensitive_words_included, BLACKLIST, WHITELIST

def test_sensitive_words_filter():
    print("🧪 开始验证敏感词安全拦截器逻辑...")

    # 1. 验证白名单的完全精确相等匹配
    print("  -> 验证白名单精确放行...")
    assert sensitive_words_included("tokenizers") is None, "白名单 tokenizers 应当放行"
    assert sensitive_words_included("keyboard.md") is None, "白名单 keyboard.md 应当放行"
    
    # 2. 验证非完全匹配白名单的项仍受黑名单严格拦截（宁多拦勿漏放原则）
    print("  -> 验证白名单非完全匹配误伤放行防护...")
    # 包含了 key 但不精准是 keyboard.md
    assert sensitive_words_included("keyboard") is not None, "仅输入 keyboard 不匹配 keyboard.md，因包含 key 应当被拦截"
    # 包含了 token 但不精准是 tokenizers
    assert sensitive_words_included("tokenizers_test") is not None, "不精准匹配 tokenizers 应当拦截"
    assert sensitive_words_included("tokenizers.md") is not None, "不精准匹配 tokenizers 应当拦截"

    # 3. 验证黑名单子包含匹配
    print("  -> 验证黑名单模糊拦截...")
    # 包含 vpn
    res_vpn = sensitive_words_included("my_vpn_tunnel")
    assert res_vpn is not None and "vpn" in res_vpn, "包含 vpn 应当被拦截"
    # 包含 tmp
    res_tmp = sensitive_words_included("temp_notes.md")
    assert res_tmp is not None and "temp" in res_tmp, "包含 temp 应当被拦截"

    # 4. 验证新增的核心隐私词拦截
    print("  -> 验证核心个人隐私词拦截...")
    # 张子兴
    res_name = sensitive_words_included("张子兴的日常.md")
    assert res_name is not None and "张子兴" in res_name, "真实姓名应当拦截"
    # 就医
    res_health = sensitive_words_included("湘雅就医记录")
    assert res_health is not None and "就医" in res_health, "就医词汇应当拦截"
    # copilot对话缓存
    res_copilot = sensitive_words_included("copilot-conversations")
    assert res_copilot is not None and "copilot-conversations" in res_copilot, "Copilot缓存应当拦截"
    # lisa主机管理与vps
    res_lisa = sensitive_words_included("lisa主机管理.md")
    assert res_lisa is not None and "lisa主机管理" in res_lisa, "主机管理词汇应当拦截"
    res_vps = sensitive_words_included("vps_notes")
    assert res_vps is not None and "vps" in res_vps, "vps资产应当拦截"

    print("✅ 敏感词安全过滤校验全部通过！白名单与黑名单行为与预期 100% 吻合！")

if __name__ == "__main__":
    test_sensitive_words_filter()
