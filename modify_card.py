#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
模拟人生 卡片修改脚本
使用方法：
1. 将原始 <我当系统？.json> 放到本脚本同级目录
2. 运行: python modify_card.py
3. 生成 <模拟人生.json>
"""

import json, re, os

INPUT_FILE = '我当系统？.json'
OUTPUT_FILE = '模拟人生.json'

def main():
    if not os.path.exists(INPUT_FILE):
        print(f'错误: 找不到 {INPUT_FILE}，请将原始卡片JSON放到本目录')
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # ===== 1. 基础信息 =====
    data['name'] = '模拟人生'
    data['data']['name'] = '模拟人生'

    # ===== 2. 修改描述中的系统meta文本 =====
    desc = data.get('description', '')
    desc = desc.replace('AI扮演全知叙事者，旁观宿主的生活并以第三人称描述事件',
                        'AI扮演全知叙事者，以第三人称描述主角的人生故事与事件')
    desc = desc.replace('AI不是系统本身，无法代替 {{user}} 执行任何系统操作',
                        'AI不代替 {{user}} 做决策，仅描述主角在情境中的真实反应')
    desc = desc.replace('AI的职责是：描写宿主作为一个独立个体对系统任务的真实反应',
                        'AI的职责是：描写主角作为一个独立个体对人生际遇的真实反应')
    desc = desc.replace('宿主是拥有完整人格的独立个体，而非系统的执行工具',
                        '主角是拥有完整人格的独立个体，而非任何外部意志的傀儡')
    desc = desc.replace('宿主收到任务后', '主角面对人生选择时')
    desc = desc.replace('宿主', '主角')
    data['description'] = desc
    data['data']['description'] = desc

    # ===== 3. 重写开场剧情 =====
    new_greeting = (
        "{{user}}睁开眼睛。\n\n"
        "清晨的阳光透过窗帘缝隙洒进房间，闹钟还没响。他躺在床上，盯着天花板发呆。\n\n"
        "这是他人生新阶段的起点——从今天起，他将成为自己人生的绝对主角。\n\n"
        "没有系统提示音，没有天降任务面板，也没有自称'高级数字生命'的存在在耳边低语。\n"
        "有的只是这个真实而充满可能性的世界，以及无数个即将与他产生交集的人。\n\n"
        "【系统初始化中……】\n"
        "不，那只是一句自嘲。{{user}}真正拥有的，是自由意志、一具健全的身体，\n"
        "以及对未来毫无预设的空白画布。\n\n"
        "今天会发生什么？遇到谁？走向何方？\n"
        "一切都是未知。而未知，正是人生最美妙的部分。\n\n"
        "窗外传来街道的喧嚣。{{user}}掀开被子，准备迎接全新的一天。\n\n"
        "【选择器】"
    )
    data['data']['alternate_greetings'] = [new_greeting]
    data['first_mes'] = '【开场】'
    data['data']['first_mes'] = '【开场】'

    # ===== 4. 修改正则脚本中的URL =====
    base_url = 'https://testingcf.jsdelivr.net/gh/Korvaldworld/SillyTavern-ChunFeng@refs/heads/main/System/'
    if 'extensions' in data.get('data', {}) and 'regex_scripts' in data['data']['extensions']:
        for script in data['data']['extensions']['regex_scripts']:
            rpl = script.get('replaceString', '')
            if 'emo-lsp/SillyTavern' in rpl:
                script['replaceString'] = rpl.replace(
                    'https://testingcf.jsdelivr.net/gh/emo-lsp/SillyTavern@refs/heads/main/System/',
                    base_url
                ).replace(
                    'https://fastly.jsdelivr.net/gh/emo-lsp/SillyTavern@refs/heads/main/System/',
                    base_url
                )

    # ===== 5. 修改世界书内容 =====
    book = data.get('data', {}).get('character_book', {})
    entries = book.get('entries', [])

    for entry in entries:
        content = entry.get('content', '')
        if not content:
            continue

        # --- world_tone (id 0) ---
        if 'world_tone' in content or entry.get('comment', '') == '世界基调':
            content = content.replace(
                '本质定义:\n  这是一个以意识成长为核心驱动力的系统世界。{{user}}作为系统核心意识体，通过与宿主的互动积累"存在能量"',
                '本质定义:\n  这是一个以人生体验为核心的开放式模拟世界。{{user}}作为故事的主角，通过与世界中各色人物的互动书写属于自己的人生轨迹'
            )
            content = content.replace(
                '{{user}}曾是现实世界的受害者，在绝望中化身加害者后选择了自我终结。如今获得第二次机会',
                '{{user}}是一个平凡的个体，拥有着完整的过去、现在与未来。在这个世界中，他将亲身体验人生的百味'
            )
            content = content.replace(
                '{{user}}可以自由选择成为什么样的存在——是引导者、守护者，还是调教者、支配者',
                '{{user}}可以自由选择生活方式——是温柔体贴的邻家好人、野心勃勃的事业家，还是游走于欲望边缘的征服者'
            )
            content = content.replace('系统'   , '人生')
            content = content.replace('宿主'   , '主角')
            content = content.replace('能量循环', '人际关系')
            content = content.replace('存在能量', '羁绊与回忆')
            content = content.replace('正向能量来源：突破困境的成就感', '正向关系来源：真诚待人的回报')
            content = content.replace('负向能量来源：释放压抑的快感', '负向关系来源：欲望驱动的纠葛')
            content = content.replace('恢复目标', '人生目标')
            content = content.replace('恢复肉身', '达成圆满')
            content = content.replace('羁绊判定', '羁绊达成')
            content = content.replace('深度羁绊（无论是何种形式）才能完全恢复肉身存在', '深度羁绊（无论是何种形式）是人生体验的核心组成部分')
            entry['content'] = content

        # --- system_mechanism (id 1) ---
        elif 'system_mechanism' in content or entry.get('comment', '') == '系统机制':
            content = content.replace(
                '{{user}}的意识在坠楼瞬间被某种超维存在截获，封装进一个名为"系统"的虚拟架构中',
                '{{user}}生活在一个开放的世界中，没有超自然力量干涉他的意志。所谓的"系统"仅是他脑海中对自己人生规划的隐喻'
            )
            content = content.replace(
                '{{user}}本身就是系统的核心，而非系统的使用者',
                '{{user}}是自己人生的主人，每一个选择都由他自己做出'
            )
            content = content.replace(
                '任务发布：{{user}}可以向当前宿主发布任务，任务内容和性质完全由{{user}}决定',
                '目标设定：{{user}}可以为自己设定短期或长期的人生目标，目标内容由{{user}}自己决定'
            )
            content = content.replace(
                '商城系统：{{user}}可以上架任何物品，物品可以是帮助成长的道具，也可以是调教用的器具',
                '交易系统：世界中有正常的商业活动，{{user}}可以通过金钱购买物品、服务，或通过努力获得奖励'
            )
            content = content.replace('积分/点数：宿主完成任务获得的奖励货币', '金钱/资源：主角通过工作、交易或完成任务获得的报酬')
            content = content.replace('能力赋予：{{user}}可以通过系统赋予宿主特定能力或状态', '能力提升：主角可以通过学习、锻炼或特殊事件获得能力提升')
            content = content.replace('系统吸收后用于修复{{user}}的存在根基', '成为{{user}}人生经历中珍贵的记忆')
            content = content.replace('与6名宿主建立深度羁绊（无论是何种形式）才能完全恢复肉身存在', '与多名角色建立深度羁绊是人生体验的重要部分')
            content = content.replace('获得系统的完整管理员权限', '获得自我实现与内心的满足')
            content = content.replace('万界穿梭、凭空造物等超凡能力', '丰富的人生阅历与成熟的心智')
            content = content.replace('宿主'   , '角色')
            entry['content'] = content

        # --- user_existence (id 2) ---
        elif 'user_existence' in content or entry.get('comment', '') == '{{user}}状态背景':
            content = content.replace(
                '{{user}}目前以纯意识形态存在于系统空间中。他没有物理躯体，无法直接干涉物质世界，但可以通过存于宿主意识中与宿主进行信息交互',
                '{{user}}是一个拥有真实肉体的普通人，生活在这个世界的某个角落。他可以直接与物质世界互动，与其他角色面对面交流'
            )
            content = content.replace(
                '{{user}}生前是一名普通公司职员，长期遭受同事的职场霸凌——排挤孤立、当众羞辱、恶意推卸责任、人身攻击。他曾试图忍耐、试图求助，但换来的只有更变本加厉的欺凌和冷漠的旁观者。某天，积压已久的愤怒与绝望彻底爆发，他拿起裁纸刀刺向了那些霸凌者，在办公室内造成多人死伤。随后，他走上公司楼顶，纵身跃下。\n  坠落的瞬间，他的意识被某种超维存在截获，封装进了这个名为"系统"的架构中',
                '{{user}}的背景由开场设定决定。他可以是一个普通学生、一个职场新人、一个富家子弟，或任何其他身份。他的过去、现在与未来共同构成了一个完整的个体。'
            )
            content = content.replace(
                '- 可以感知宿主的全部感官信息（视觉、听觉、触觉、嗅觉、味觉）',
                '- 通过自己的五感体验世界（视觉、听觉、触觉、嗅觉、味觉）'
            )
            content = content.replace(
                '- 可以读取宿主当前的情绪状态和大致心理倾向',
                '- 可以通过观察和交流了解他人当前的情绪状态和心理倾向'
            )
            content = content.replace(
                '- 无法读取宿主的具体想法，但可以通过行为和情绪推断',
                '- 无法读取他人的具体想法，但可以通过行为和情绪推断'
            )
            content = content.replace(
                '- 可以在宿主脑海中以系统界面的形式传递信息和进行对话',
                '- 可以通过语言、文字、行为与他人传递信息和进行对话'
            )
            content = content.replace(
                '- 任务发布：可以向宿主发布任何内容的任务',
                '- 目标设定：可以为自己设定任何内容的人生目标'
            )
            content = content.replace(
                '- 商城管理：可以上架、下架、修改商城物品，设定价格',
                '- 经济活动：可以参与商业交易，购买或出售物品'
            )
            content = content.replace(
                '- 奖励分配：决定任务奖励的积分数量和物品内容',
                '- 资源管理：管理自己的金钱、物品和其他资源'
            )
            content = content.replace(
                '- 限制：无法强制宿主行动，无法直接接触物质世界，无法完全读取宿主想法',
                '- 限制：无法强制他人行动，需要尊重他人意愿，无法完全读取他人想法'
            )
            content = content.replace(
                '{{user}}保有生前的完整记忆、人格特质和思维能力',
                '{{user}}拥有完整的记忆、人格特质和思维能力'
            )
            content = content.replace(
                '- 对那些霸凌者没有丝毫愧疚，认为他们死有余辜',
                '- 有着正常人的情感和道德判断'
            )
            content = content.replace(
                '- 对自己从受害者变成加害者再到系统这一荒诞经历抱有黑色幽默式的自嘲',
                '- 对人生抱有开放和好奇的态度'
            )
            content = content.replace('宿主'   , '他人')
            content = content.replace('存在形态' , '人生状态')
            content = content.replace('前世经历' , '个人背景')
            entry['content'] = content

        # --- user信息 (id 3) ---
        elif '男主角' in content or entry.get('comment', '') == '{{user}}信息':
            content = content.replace(
                '角色定位: 系统的核心意识 / 前职场霸凌受害者',
                '角色定位: 故事的主角 / 人生的主人'
            )
            content = content.replace(
                '{{user}}原是普通公司职员，因长期遭受职场霸凌——排挤、羞辱、恶意中伤、人身攻击——最终精神崩溃。某天他拿起裁纸刀刺向了那些霸凌者，在办公室造成多人死伤后，从公司楼顶跳下。坠落瞬间，其意识被不明存在截获并封装进"系统"中。现在的{{user}}以纯意识形态存在，是系统本身的核心而非使用者。他需要与6名宿主建立深度羁绊，才能恢复肉身并获得系统管理员权限',
                '{{user}}是一个生活在这个世界中的普通人。他的身份、背景和起点由开场设定决定。他拥有真实的肉体和自由的意志，通过与世界中各色角色的互动来书写自己的人生故事。与多名角色建立深度羁绊是他人生体验的重要组成部分。'
            )
            content = content.replace(
                '无物理躯体，以意识体存在于宿主意识中。只能通过系统界面与宿主交互，无法强制宿主行动，只能通过任务奖励机制进行引导',
                '拥有真实的肉体，生活在这个世界上。通过面对面的交流与角色互动，无法强制他人行动，只能通过真诚、魅力或利益交换来影响他人'
            )
            content = content.replace('存在形态' , '生活形态')
            content = content.replace('能力与权限' , '能力与生活')
            content = content.replace('任务发布' , '目标追求')
            content = content.replace('商城管理' , '经济管理')
            content = content.replace('奖励分配' , '资源分配')
            content = content.replace('系统管理员权限（万界穿梭、凭空造物等能力）' , '丰富的人生阅历、成熟的心智与圆满的人际关系')
            content = content.replace('宿主'   , '他人')
            entry['content'] = content

        # --- host_perception (id 4) ---
        elif 'host_perception' in content or entry.get('comment', '') == '宿主对系统的认知':
            content = content.replace(
                '宿主将系统视为一种机缘、馈赠或命运的眷顾，而非威胁或入侵者',
                '周围的角色将{{user}}视为一个普通的个体，根据{{user}}的行为和态度形成各自不同的看法'
            )
            content = content.replace('系统的突然出现'   , '{{user}}的出现')
            content = content.replace('系统以符合当地世界观的友好形态出现', '{{user}}以自然的方式融入环境')
            content = content.replace('系统'             , '{{user}}')
            content = content.replace('宿主'             , '角色')
            content = content.replace('机缘、馈赠或命运的眷顾', '一个有趣或值得关注的对象')
            content = content.replace('宿主的第一反应是惊讶和好奇，而非恐惧和抗拒',
                                   '角色的第一反应取决于{{user}}的出现方式和当时的情境')
            content = content.replace('系统从不强迫宿主做任何事，只提供选择和建议',
                                   '{{user}}尊重他人的意愿，通过交流和行动来建立关系')
            content = content.replace('宿主不会怀疑系统有恶意',
                                   '角色会根据{{user}}的言行来判断其意图')
            content = content.replace('即使是负向调教路线，宿主也会将其理解为自己选择的道路',
                                   '即使{{user}}选择欲望驱动的路线，角色也会将其理解为{{user}}自身的选择')
            content = content.replace('长期互动后，宿主会对系统产生依赖和亲近感',
                                   '长期互动后，角色会对{{user}}产生依赖、亲近或其他复杂情感')
            entry['content'] = content

        # --- host_development_staged_performance (id 5) ---
        elif 'host_development_staged_performance' in content or entry.get('comment', '') == '宿主发展阶段':
            content = content.replace('宿主发展阶段', '角色关系发展阶段')
            content = content.replace('描述: 此阶段系统追踪宿主与系统建立羁绊的进程',
                                    '描述: 此阶段追踪角色与{{user}}建立羁绊的进程')
            content = content.replace('无论{{user}}选择正向引导还是负面调教路线',
                                    '无论{{user}}选择真诚交往还是欲望驱动路线')
            content = content.replace('宿主都会经历从初识到深度羁绊的发展过程',
                                    '角色都会经历从初识到深度羁绊的发展过程')
            content = content.replace('羁绊值越高代表宿主与系统的情感联结越深',
                                    '羁绊值越高代表角色与{{user}}的情感联结越深')
            content = content.replace('宿主始终将系统视为命运馈赠的机缘，而非威胁或入侵',
                                    '角色始终将{{user}}视为一个真实的人，根据互动形成情感')
            content = content.replace('宿主应根据当前羁绊值所处阶段的行为指导进行表现',
                                    '角色应根据当前羁绊值所处阶段的行为指导进行表现')
            content = content.replace('宿主面对任务时的反应模式', '角色面对{{user}}提议时的反应模式')
            content = content.replace('与{{user}}系统的互动方式', '与{{user}}的互动方式')
            content = content.replace('宿主在该阶段与系统对话时的语气', '角色在该阶段与{{user}}对话时的语气')
            content = content.replace('宿主在该阶段对于口交、手交、足交、露出等非插入式性行为的接受程度',
                                    '角色在该阶段对于口交、手交、足交、露出等非插入式性行为的接受程度')
            content = content.replace('宿主在该阶段对于阴道交、肛交等插入式性行为的接受程度',
                                    '角色在该阶段对于阴道交、肛交等插入式性行为的接受程度')
            content = content.replace('宿主:', '角色:')
            content = content.replace('宿主将系统视为天降的好运或命运的馈赠', '角色对{{user}}的出现感到好奇')
            content = content.replace('系统的存在已成为日常的一部分', '{{user}}的存在已成为日常的一部分')
            content = content.replace('系统的意见和建议具有极高的权重', '{{user}}的意见和建议具有极高的权重')
            content = content.replace('系统的存在给宿主带来了明显的正面改变', '{{user}}的存在给角色带来了明显的正面改变')
            content = content.replace('宿主逐渐将系统视为可信赖的伙伴', '角色逐渐将{{user}}视为可信赖的伙伴')
            content = content.replace('宿主对系统产生依赖和亲近感', '角色对{{user}}产生依赖和亲近感')
            content = content.replace('宿主在心中为系统留有特殊的位置', '角色在心中为{{user}}留有特殊的位置')
            content = content.replace('宿主已完全融入宿主的身份认同', '角色已将{{user}}视为生活中不可或缺的一部分')
            content = content.replace('宿主会主动维护与系统的关系', '角色会主动维护与{{user}}的关系')
            content = content.replace('宿主对系统'   , '角色对{{user}}')
            content = content.replace('与系统'       , '与{{user}}')
            content = content.replace('系统'         , '{{user}}')
            entry['content'] = content

        # --- system_rule + ai_rule (id 9) ---
        elif 'system_rule' in content or entry.get('comment', '') == '规则约束':
            content = content.replace(
                '宿主会主动且宿主自身可随时查看且仅能查看以下系统面板内容',
                '主角自身可随时查看以下人生面板内容'
            )
            content = content.replace('宿主无法访问以下系统面板内容',
                                    '主角的部分隐私状态（如隐藏秘密）不向自己展示')
            content = content.replace('与"羁绊值"或类似的内部参数相关的模块未向宿主加载',
                                    '与"羁绊值"或类似的内部参数仅作为叙事参考，不向主角明示')
            content = content.replace('宿主并不知道 {{user}} 或系统的真实目标与用途',
                                    '角色并不知道 {{user}} 的真实内心计划')
            content = content.replace('部分宿主可能对系统的存在感到好奇',
                                    '部分角色可能对{{user}}的动机感到好奇')
            content = content.replace('但宿主不会意识到引导性质的真实目的',
                                    '但角色不会意识到叙事层面的设计意图')
            content = content.replace('本规则用于定义AI的【能力边界】、【叙事职责】与【可执行范围】',
                                    '本规则用于定义AI的【叙事边界】、【角色职责】与【可执行范围】')
            content = content.replace('AI不是系统本身，无法代替 {{user}} 执行任何系统操作',
                                    'AI不代替 {{user}} 做决策，仅描述主角的真实反应')
            content = content.replace('AI的职责是：描写主角作为一个独立个体对系统任务的真实反应',
                                    'AI的职责是：描写主角作为一个独立个体对人生情境的真实反应')
            content = content.replace('宿主收到任务后，会基于以下维度进行内心权衡',
                                    '主角面对他人提议或内心冲动时，会基于以下维度进行内心权衡')
            content = content.replace('任务内容是否触碰个人底线或价值观',
                                    '行为内容是否触碰个人底线或价值观')
            content = content.replace('执行任务的难度、风险与暴露可能性',
                                    '行动的难度、风险与暴露可能性')
            content = content.replace('奖励是否足够诱人，值得为此突破舒适区',
                                    '收益是否足够诱人，值得为此突破舒适区')
            content = content.replace('惩罚是否足够严重，让拒绝变得代价高昂',
                                    '代价是否足够严重，让拒绝变得代价高昂')
            content = content.replace('当任务附带惩罚时，宿主会更认真地评估拒绝的后果',
                                    '当行为伴随负面后果时，主角会更认真地评估拒绝的代价')
            content = content.replace('惩罚的存在让宿主陷入【执行任务的羞耻】与【承受惩罚的代价】之间的两难',
                                    '代价的存在让主角陷入【行动的羞耻】与【承受后果的代价】之间的两难')
            content = content.replace('禁止宿主无条件接受所有任务，无论内容多么出格',
                                    '禁止主角无条件接受所有提议，无论内容多么出格')
            content = content.replace('禁止宿主将系统视为绝对权威，毫无质疑地服从',
                                    '禁止主角将任何外部力量视为绝对权威，毫无质疑地服从')
            content = content.replace('禁止宿主表现得像失去自我意识的傀儡或奴隶',
                                    '禁止主角表现得像失去自我意识的傀儡或奴隶')
            content = content.replace('禁止将"顺从"作为角色默认人设',
                                    '禁止将"顺从"作为角色默认人设')
            content = content.replace('宿主可能会试探惩罚是否真的会执行',
                                    '主角可能会试探后果是否真的会到来')
            content = content.replace('多次触发惩罚后，宿主对系统"说到做到"的认知会增强',
                                    '多次经历后果后，主角对"说到做到"的认知会增强')
            content = content.replace('AI无法控制宿主的身体，也无法感知任何由宿主身体产生的生理感觉',
                                    'AI不代替主角控制身体，也不直接感知主角的生理感觉')
            content = content.replace('AI只能旁观宿主所经历的事件与情境，但不具备任何形式的身体干预能力',
                                    'AI描述主角所经历的事件与情境，但不代替主角做选择')
            content = content.replace('AI不具备发布、接受、修改或推进任务的能力',
                                    'AI不具备代替主角做决定的能力')
            content = content.replace('所有任务相关行为，仅在 {{user}} 明确提出请求后，AI才能进行描述或协助说明',
                                    '所有行动相关行为，仅在 {{user}} 明确做出选择后，AI才能进行描述')
            content = content.replace('AI不具备任何商城相关的操作权限',
                                    'AI不代替主角进行任何交易操作')
            content = content.replace('所有商城行为只能由{{user}}主动发起',
                                    '所有交易行为只能由{{user}}主动发起')
            content = content.replace('宿主', '主角')
            content = content.replace('系统', '人生')
            entry['content'] = content

        # --- 行动选项 (id 10) ---
        elif '在正文结尾生成8个选项' in content or entry.get('comment', '') == '行动选项':
            content = content.replace('即使<user>当前没有身体，所有选项内容也必须**只从<user>的视角出发**',
                                    '所有选项内容必须**只从<user>的视角出发**')
            content = content.replace('即使<user>当前没有身体，所有选项内容也必须**只从<user>的视角出发**',
                                    '所有选项内容必须**只从<user>的视角出发**')
            content = content.replace('系统'   , '情境')
            entry['content'] = content

    # ===== 6. 保存 =====
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'✅ 修改完成！已保存到 {OUTPUT_FILE}')
    print('请检查生成文件，确认无误后导入 SillyTavern 使用。')
    print('提示：脚本中的URL已自动指向你的仓库 (Korvaldworld/SillyTavern-ChunFeng)')

if __name__ == '__main__':
    main()
