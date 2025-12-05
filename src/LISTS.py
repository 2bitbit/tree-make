# 敏感词黑名单 (包含这些词的路径会被过滤)
_BLACKLIST = {
    "灰产",
    "fullz",
    "梯子",
    "VPN",
    "破解",
    "盗版",
    "password",
    "private",
    "key",
    "token",
    "tmp",
    "未命名",
    "temp",
}
_WHITELIST = {
    "keyboard.md",
}


def sensitive_words_included(name: str) -> None|list:
    """检查名称:
    - 是否因包含敏感词而在黑名单中
    - 是否在白名单中
    
    Returns:
        - None 未包含敏感词，允许通过 
        - list 包含的敏感词列表
    """
    lower_name = name.lower()
    is_in_whitelist = lower_name in _WHITELIST
    if is_in_whitelist:
        return None
    words_in_blacklist = [word for word in _BLACKLIST if word in lower_name]
    if words_in_blacklist:
        return words_in_blacklist
    else:
        return None