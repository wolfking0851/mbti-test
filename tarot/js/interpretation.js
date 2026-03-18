// 塔罗牌解读内容库 - 完整版
// 包含 22 张大阿卡纳完整解读 + 56 张小阿卡纳完整解读

/**
 * 获取单张牌的解读
 */
function getCardReading(card, positionIndex) {
    const positionNames = ['过去', '现在', '未来'];
    const positionName = positionNames[positionIndex];
    
    const baseReading = getBaseCardMeaning(card.id, card.position);
    
    let html = `
        <p><strong>📍 位置：</strong>${positionName}</p>
        <p><strong>✨ 状态：</strong>${card.position === 'upright' ? '正位' : '逆位'}</p>
        <p><strong>🔑 关键词：</strong>${baseReading.keywords.join(' · ')}</p>
        <hr style="border:0; border-top:1px solid rgba(144,202,249,0.3); margin:15px 0;">
        <p style="line-height:1.8;">${baseReading.meaning}</p>
        <p style="margin-top:15px; color:#64b5f6;"><strong>💡 建议：</strong>${baseReading.advice}</p>
    `;
    
    return html;
}

/**
 * 22 张大阿卡纳完整解读
 */
const majorArcana = {
    0: {
        name: '愚人',
        upright: {
            keywords: ['新的开始', '冒险精神', '自由', '无限可能'],
            meaning: '愚人正位代表全新的开始和冒险精神。你正站在人生的新起点，前方充满无限可能。放下过去的束缚，跟随内心的指引，勇敢迈出第一步。',
            advice: '保持开放好奇的心态，勇敢尝试，但保持基本安全意识。'
        },
        reversed: {
            keywords: ['鲁莽', '冲动', '冒险', '不负责任'],
            meaning: '愚人逆位提醒你需要谨慎行事。你可能过于冲动，没有充分考虑后果。现在不是盲目行动的最佳时机。',
            advice: '行动前多做思考和规划，评估风险，不要完全凭直觉。'
        }
    },
    1: {
        name: '魔术师',
        upright: {
            keywords: ['创造力', '技能', '自信', '显化'],
            meaning: '魔术师正位代表你拥有实现目标所需的一切资源和能力。这是展现才华、发挥影响力、将想法转化为现实的好时机。',
            advice: '相信自己的能力，积极行动，利用现有资源将计划付诸实践。'
        },
        reversed: {
            keywords: ['欺骗', '犹豫', '能力不足', '浪费潜力'],
            meaning: '魔术师逆位暗示你可能没有充分发挥潜力，或在使用能力时不够诚实。存在自我怀疑或能力不足的感觉。',
            advice: '重新审视动机，确保诚实。提升技能，增强自信，避免投机取巧。'
        }
    },
    2: {
        name: '女祭司',
        upright: {
            keywords: ['直觉', '潜意识', '智慧', '神秘'],
            meaning: '女祭司正位代表直觉和内在智慧的觉醒。倾听内心的声音，相信自己的直觉。这是适合内省、冥想和精神成长的时期。',
            advice: '给自己独处时间，倾听内心声音。记录梦境和直觉，它们可能带来重要启示。'
        },
        reversed: {
            keywords: ['忽视直觉', '情绪化', '表面化', '判断失误'],
            meaning: '女祭司逆位表示你可能忽视了自己的直觉，或过于情绪化而无法清晰思考。可能被表面现象迷惑。',
            advice: '重新连接直觉，避免被情绪左右。深入思考问题本质，不要急于下结论。'
        }
    },
    3: {
        name: '皇后',
        upright: {
            keywords: ['丰饶', '创造力', '母性', '自然'],
            meaning: '皇后正位象征丰饶、创造力和母性能量。你可能正处于富有创造力和生产力的时期，工作、艺术或人际关系都在蓬勃发展。',
            advice: '拥抱创造力，滋养项目和人脉。关注感官享受和自然之美，享受劳动成果。'
        },
        reversed: {
            keywords: ['依赖', '创造力受阻', '过度保护', '浪费'],
            meaning: '皇后逆位可能表示创造力受阻，或过度依赖他人。可能存在过度保护、控制欲强或浪费资源的情况。',
            advice: '重新审视创造项目，找到阻碍根源。学会放手，给予他人成长空间。'
        }
    },
    4: {
        name: '皇帝',
        upright: {
            keywords: ['权威', '稳定', '秩序', '领导力'],
            meaning: '皇帝正位代表权威、稳定和秩序。你可能处于需要展现领导力和控制力的位置。这是建立规则、实现目标的时期。',
            advice: '展现领导才能，制定清晰计划和规则。保持自律和责任感。'
        },
        reversed: {
            keywords: ['专制', '僵化', '缺乏控制', '软弱'],
            meaning: '皇帝逆位可能表示过度控制或专制，也可能暗示缺乏领导力和决断力。需要找到平衡点。',
            advice: '反思领导方式，避免过度控制或过于软弱。学会灵活应对。'
        }
    },
    5: {
        name: '教皇',
        upright: {
            keywords: ['传统', '信仰', '指导', '学习'],
            meaning: '教皇正位代表传统价值观、精神指导和学习。你可能正在寻求更高层次的理解，或需要导师的指引。',
            advice: '尊重传统和智慧，寻求导师指导。这是学习和精神成长的好时机。'
        },
        reversed: {
            keywords: ['反传统', '自由思考', '挑战权威', '非主流'],
            meaning: '教皇逆位表示你可能挑战传统观念，或寻找非主流的精神路径。可能质疑现有权威和规则。',
            advice: '保持开放心态，但也要尊重他人信仰。找到适合自己的精神路径。'
        }
    },
    6: {
        name: '恋人',
        upright: {
            keywords: ['爱情', '选择', '和谐', '关系'],
            meaning: '恋人正位代表爱情、和谐的关系和重要的选择。你可能面临一个需要听从内心的决定，或在关系中获得深层连接。',
            advice: '倾听内心的声音，做出符合真实自我的选择。珍惜重要的人际关系。'
        },
        reversed: {
            keywords: ['关系问题', '选择困难', '不和谐', '分离'],
            meaning: '恋人逆位可能表示关系出现问题，或在选择上感到困惑。可能存在价值观冲突或沟通障碍。',
            advice: '诚实地面对关系问题，加强沟通。在做决定前理清自己的价值观。'
        }
    },
    7: {
        name: '战车',
        upright: {
            keywords: ['胜利', '意志力', '决心', '进展'],
            meaning: '战车正位代表通过意志力和决心获得胜利。你正在克服困难，朝着目标稳步前进。这是展现自律和专注的时刻。',
            advice: '保持专注和自律，坚定地朝着目标前进。相信你有能力克服障碍。'
        },
        reversed: {
            keywords: ['失败', '缺乏方向', '失控', '挫折'],
            meaning: '战车逆位可能表示失去方向感，或无法控制局面。可能遇到挫折或感到力不从心。',
            advice: '重新评估目标和策略。学会放手，不要强行控制一切。'
        }
    },
    8: {
        name: '力量',
        upright: {
            keywords: ['勇气', '耐心', '内在力量', '同情心'],
            meaning: '力量正位代表内在的勇气和耐心。你拥有克服困难所需的内在力量，能够以温柔和同情心面对挑战。',
            advice: '相信自己的内在力量，用耐心和同情心面对挑战。温柔比强硬更有效。'
        },
        reversed: {
            keywords: ['自我怀疑', '软弱', '恐惧', '缺乏信心'],
            meaning: '力量逆位表示你可能怀疑自己的能力，或被恐惧和不安所困扰。需要重新连接内在力量。',
            advice: '承认自己的恐惧，但不要让它控制你。从小事开始重建信心。'
        }
    },
    9: {
        name: '隐士',
        upright: {
            keywords: ['内省', '智慧', '独处', '寻找真理'],
            meaning: '隐士正位代表内省和寻找内在智慧的时期。你需要独处时间来思考人生的意义，寻找内心的答案。',
            advice: '给自己独处的时间，深入思考。答案在你内心，不在外界。'
        },
        reversed: {
            keywords: ['孤立', '逃避', '拒绝帮助', '迷失'],
            meaning: '隐士逆位可能表示过度孤立自己，或逃避必要的社交。可能拒绝他人的帮助和建议。',
            advice: '平衡独处和社交时间。不要拒绝善意的帮助，有时他人能提供有价值的视角。'
        }
    },
    10: {
        name: '命运之轮',
        upright: {
            keywords: ['变化', '命运', '转折点', '周期'],
            meaning: '命运之轮正位代表重要的转折点和命运的变化。生活正在发生转变，可能是好运的到来。接受变化，顺应潮流。',
            advice: '拥抱变化，相信宇宙的安排。这是新的开始，保持积极心态。'
        },
        reversed: {
            keywords: ['阻力', '延迟', '抗拒变化', '坏运气'],
            meaning: '命运之轮逆位表示你可能在抗拒必要的变化，或感到运气不佳。变化仍在发生，但你可能感到阻力。',
            advice: '放下抗拒，接受变化是生活的一部分。耐心等待，坏运气终会过去。'
        }
    },
    11: {
        name: '正义',
        upright: {
            keywords: ['公平', '真理', '法律', '因果'],
            meaning: '正义正位代表公平、真理和因果平衡。你需要做出公正的决定，或即将看到事情的真实面貌。',
            advice: '保持客观和公正，做出符合良心的决定。真相终将大白。'
        },
        reversed: {
            keywords: ['不公平', '偏见', '逃避责任', '失衡'],
            meaning: '正义逆位可能表示不公平的情况，或你在逃避责任。可能存在偏见或判断失误。',
            advice: '审视自己的偏见，承担应有的责任。努力恢复平衡和公正。'
        }
    },
    12: {
        name: '倒吊人',
        upright: {
            keywords: ['牺牲', '换位思考', '等待', '新视角'],
            meaning: '倒吊人正位代表需要牺牲和换位思考的时期。可能需要暂时放下某些东西，从不同角度看待问题。',
            advice: '学会放手，从不同角度看问题。有时候等待和牺牲是必要的。'
        },
        reversed: {
            keywords: ['无谓牺牲', '拖延', '抗拒', '自我中心'],
            meaning: '倒吊人逆位表示你可能在做无谓的牺牲，或过度拖延。可能抗拒必要的改变，过于自我中心。',
            advice: '评估你的牺牲是否值得。不要拖延必要的决定，学会为他人着想。'
        }
    },
    13: {
        name: '死神',
        upright: {
            keywords: ['结束', '转变', '释放', '重生'],
            meaning: '死神正位代表重要的结束和转变。某个生活阶段即将结束，为新的开始腾出空间。这是释放过去、迎接新生的时刻。',
            advice: '接受必要的结束，不要执着于过去。相信转变后会迎来更好的开始。'
        },
        reversed: {
            keywords: ['抗拒改变', '停滞', '无法放手', '恐惧'],
            meaning: '死神逆位表示你可能在抗拒必要的改变，或无法放手过去。这种抗拒可能导致停滞不前。',
            advice: '认识到改变是不可避免的。学会放手，才能迎接新的可能性。'
        }
    },
    14: {
        name: '节制',
        upright: {
            keywords: ['平衡', '调和', '耐心', '适度'],
            meaning: '节制正位代表平衡和调和。你需要找到生活的平衡点，避免极端。这是培养耐心和适度态度的时期。',
            advice: '寻找平衡点，避免走极端。保持耐心，循序渐进地前进。'
        },
        reversed: {
            keywords: ['失衡', '过度', '缺乏耐心', '冲突'],
            meaning: '节制逆位表示生活可能失去平衡，或你在某方面过度投入。可能存在内心冲突或缺乏耐心。',
            advice: '重新评估优先级，恢复生活平衡。学会适度，避免过度消耗。'
        }
    },
    15: {
        name: '恶魔',
        upright: {
            keywords: ['束缚', '欲望', '物质', '沉迷'],
            meaning: '恶魔正位代表被物质欲望或不良习惯所束缚。你可能感到被困住，无法摆脱某些负面模式。',
            advice: '认识到你有选择的力量。审视哪些信念或习惯在限制你，勇敢打破束缚。'
        },
        reversed: {
            keywords: ['解脱', '觉醒', '打破束缚', '自由'],
            meaning: '恶魔逆位代表你正在打破束缚，获得自由。你开始认识到自己的力量，摆脱负面模式。',
            advice: '继续走向自由，不要回头。相信自己有能力过更好的生活。'
        }
    },
    16: {
        name: '高塔',
        upright: {
            keywords: ['突变', '启示', '崩溃', '觉醒'],
            meaning: '高塔正位代表突如其来的变化和启示。某些信念或结构可能突然崩溃，但这是为了重建更真实的基础。',
            advice: '接受必要的改变，即使它来得突然。废墟之上会建立更坚固的基础。'
        },
        reversed: {
            keywords: ['避免灾难', '延迟改变', '恐惧', '挣扎'],
            meaning: '高塔逆位表示你可能在避免必要的改变，或改变被延迟了。你可能感到恐惧和挣扎。',
            advice: '认识到改变是必要的，早变比晚变好。主动迎接改变，而不是被动承受。'
        }
    },
    17: {
        name: '星星',
        upright: {
            keywords: ['希望', '灵感', '平静', '治愈'],
            meaning: '星星正位代表希望、灵感和内心的平静。经历困难后，你重新找到方向和信心。这是治愈和恢复的时期。',
            advice: '保持希望和信心，相信未来。跟随你的灵感，它会带你走向正确的方向。'
        },
        reversed: {
            keywords: ['绝望', '缺乏信心', '迷失', '沮丧'],
            meaning: '星星逆位表示你可能感到绝望或失去信心。可能觉得前路迷茫，找不到方向。',
            advice: '给自己时间恢复，不要强迫自己立刻振作。小步前进，信心会逐渐恢复。'
        }
    },
    18: {
        name: '月亮',
        upright: {
            keywords: ['幻觉', '恐惧', '潜意识', '直觉'],
            meaning: '月亮正位代表幻觉、恐惧和潜意识的浮现。你可能感到困惑，看不清真相。这是探索内心深处的时期。',
            advice: '相信你的直觉，但也要区分事实和想象。面对恐惧，它们往往没有想象中可怕。'
        },
        reversed: {
            keywords: ['清晰', '真相', '恐惧消散', '理解'],
            meaning: '月亮逆位表示困惑正在消散，真相逐渐清晰。恐惧和不安开始减轻。',
            advice: '拥抱清晰和理解，相信自己的判断。走出迷雾，迎接光明。'
        }
    },
    19: {
        name: '太阳',
        upright: {
            keywords: ['成功', '快乐', '活力', '光明'],
            meaning: '太阳正位代表成功、快乐和活力。你正处于充满阳光和正能量的时期，一切都显得美好。',
            advice: '享受当下的快乐，分享你的正能量。这是实现目标和获得认可的时期。'
        },
        reversed: {
            keywords: ['暂时的阴霾', '缺乏热情', '延迟的成功', '内省'],
            meaning: '太阳逆位表示你可能暂时感到缺乏热情，或成功被延迟。但这只是暂时的阴霾。',
            advice: '保持耐心，阳光终会再现。利用这段时间内省和准备。'
        }
    },
    20: {
        name: '审判',
        upright: {
            keywords: ['觉醒', '重生', '召唤', '宽恕'],
            meaning: '审判正位代表觉醒和重生。你听到内心的召唤，准备迎接新的生活阶段。这是宽恕和释放的时刻。',
            advice: '回应内心的召唤，放下过去的包袱。原谅自己和他人，迎接新生。'
        },
        reversed: {
            keywords: ['拒绝召唤', '自我怀疑', '未解决的过去', '拖延'],
            meaning: '审判逆位表示你可能拒绝内心的召唤，或被过去的未解决问题所困扰。存在自我怀疑。',
            advice: '面对未解决的过去，做出必要的改变。不要拖延人生的重要决定。'
        }
    },
    21: {
        name: '世界',
        upright: {
            keywords: ['完成', '成就', '圆满', '新开始'],
            meaning: '世界正位代表完成和成就。一个重要的周期即将结束，你达成了目标。这是庆祝和准备新开始的时刻。',
            advice: '庆祝你的成就，感恩一路走来的经历。准备好迎接新的周期。'
        },
        reversed: {
            keywords: ['未完成', '延迟', '缺乏进展', '不满足'],
            meaning: '世界逆位表示某个周期尚未完成，或你感到不满足。可能缺乏进展或遇到延迟。',
            advice: '完成未完成的事情，不要急于开始新的。找到 closure，再前进。'
        }
    }
};

/**
 * 56 张小阿卡纳完整解读
 */
const minorArcana = {
    // ========== 权杖组（火元素）- 22-35 ==========
    22: { name: '权杖 Ace', suit: 'wands', upright: { keywords: ['新机会', '激情', '创造力'], meaning: '新的开始和机会出现，充满激情和创造力。这是启动新项目、追求梦想的好时机。', advice: '抓住机会，积极行动，让激情指引你前进。' }, reversed: { keywords: ['延迟', '阻碍', '缺乏动力'], meaning: '计划可能遇到延迟或阻碍，或缺乏行动的动力。需要重新评估目标。', advice: '耐心等待，重新评估计划，找到内在动力。' } },
    23: { name: '权杖 2', suit: 'wands', upright: { keywords: ['规划', '决定', '远见'], meaning: '需要做出重要决定，规划未来方向。你站在十字路口，需要选择前进的道路。', advice: '权衡利弊，做出明智选择，相信自己的判断。' }, reversed: { keywords: ['犹豫', '恐惧', '缺乏计划'], meaning: '可能犹豫不决或缺乏明确计划，害怕做出错误决定。', advice: '克服恐惧，制定清晰计划，相信直觉。' } },
    24: { name: '权杖 3', suit: 'wands', upright: { keywords: ['扩张', '进展', '远见'], meaning: '你的努力开始见到成效，事业或项目正在扩张。展望未来，充满希望。', advice: '继续前进，扩大视野，把握增长机会。' }, reversed: { keywords: ['挫折', '延迟', '缺乏进展'], meaning: '可能遇到挫折或进展缓慢，感到沮丧。需要重新调整策略。', advice: '保持耐心，调整策略，不要放弃长远目标。' } },
    25: { name: '权杖 4', suit: 'wands', upright: { keywords: ['庆祝', '稳定', '和谐'], meaning: '这是一个值得庆祝的时刻，生活稳定和谐。享受劳动成果，与亲友分享喜悦。', advice: '停下来庆祝成就，感恩身边的人和事。' }, reversed: { keywords: ['不稳定', '冲突', '无法放松'], meaning: '可能感到不稳定或有冲突，无法放松享受。需要找到平衡。', advice: '解决冲突，创造和谐环境，允许自己放松。' } },
    26: { name: '权杖 5', suit: 'wands', upright: { keywords: ['竞争', '冲突', '挑战'], meaning: '可能面临竞争或冲突，需要为立场而战。这是考验能力和决心的时刻。', advice: '勇敢面对挑战，但避免不必要的冲突。' }, reversed: { keywords: ['避免冲突', '妥协', '内在斗争'], meaning: '可能试图避免冲突，或正在进行内在斗争。需要找到和平解决方案。', advice: '寻求妥协，解决内在冲突，找到平衡点。' } },
    27: { name: '权杖 6', suit: 'wands', upright: { keywords: ['胜利', '认可', '成就'], meaning: '你获得了胜利和认可，努力得到回报。这是值得骄傲和庆祝的时刻。', advice: '享受成功的喜悦，但不要骄傲自满。' }, reversed: { keywords: ['失败', '缺乏认可', '骄傲'], meaning: '可能感到失败或缺乏认可，或过于骄傲。需要调整心态。', advice: '从失败中学习，保持谦逊，继续努力。' } },
    28: { name: '权杖 7', suit: 'wands', upright: { keywords: ['坚持', '勇气', '挑战'], meaning: '你正在坚持自己的立场，勇敢面对挑战。需要勇气和毅力来维持优势。', advice: '坚持到底，相信自己的能力，不要退缩。' }, reversed: { keywords: ['放弃', '屈服', '疲惫'], meaning: '可能感到疲惫，想要放弃或屈服。需要重新找回力量。', advice: '休息后重新出发，寻求支持，不要独自承担。' } },
    29: { name: '权杖 8', suit: 'wands', upright: { keywords: ['速度', '行动', '消息'], meaning: '事情进展迅速，可能有重要消息到来。这是快速行动的时期。', advice: '把握时机，迅速行动，不要犹豫。' }, reversed: { keywords: ['延迟', '沟通问题', '匆忙'], meaning: '可能遇到延迟或沟通问题，或过于匆忙。需要放慢脚步。', advice: '检查沟通是否清晰，避免匆忙决定。' } },
    30: { name: '权杖 9', suit: 'wands', upright: { keywords: ['毅力', '防御', '坚持'], meaning: '你正在坚持防守，虽然疲惫但没有放弃。需要毅力来度过难关。', advice: '坚持下去，胜利就在前方。适当休息，保持警惕。' }, reversed: { keywords: ['放弃', '疲惫', '失去警惕'], meaning: '可能感到极度疲惫，想要放弃。或失去警惕，容易受攻击。', advice: '寻求支持，不要独自承担。重新评估是否值得继续。' } },
    31: { name: '权杖 10', suit: 'wands', upright: { keywords: ['负担', '责任', '压力'], meaning: '你承担了过多责任，感到压力重重。虽然接近目标，但负担过重。', advice: '学会 delegating，不要承担所有责任。适当减负。' }, reversed: { keywords: ['释放负担', '崩溃', '逃避'], meaning: '可能到了崩溃边缘，需要释放负担。或在逃避责任。', advice: '放下不必要的负担，寻求他人帮助。' } },
    32: { name: '权杖侍从', suit: 'wands', upright: { keywords: ['探索', '热情', '新想法'], meaning: '新的想法和热情涌现，想要探索未知。这是学习和成长的时期。', advice: '追随你的热情，勇于尝试新事物。' }, reversed: { keywords: ['分心', '拖延', '缺乏方向'], meaning: '可能分心或缺乏方向，拖延行动。需要聚焦目标。', advice: '聚焦一个目标，避免分心，立即行动。' } },
    33: { name: '权杖骑士', suit: 'wands', upright: { keywords: ['行动', '冒险', '冲劲'], meaning: '充满行动力和冒险精神，勇往直前。这是追求目标的时期。', advice: '保持冲劲，但也要考虑后果。' }, reversed: { keywords: ['鲁莽', '急躁', '受阻'], meaning: '可能过于鲁莽急躁，或行动受阻。需要冷静思考。', advice: '冷静下来，制定计划后再行动。' } },
    34: { name: '权杖皇后', suit: 'wands', upright: { keywords: ['自信', '魅力', '独立'], meaning: '你充满自信和魅力，独立自主。能够吸引他人并影响他们。', advice: '发挥你的领导力和魅力，激励他人。' }, reversed: { keywords: ['控制欲', '嫉妒', '缺乏自信'], meaning: '可能表现出控制欲或嫉妒，或缺乏自信。需要平衡。', advice: '放下控制，相信他人。重建自信。' } },
    35: { name: '权杖国王', suit: 'wands', upright: { keywords: ['领导力', '远见', '决断'], meaning: '你展现出强大的领导力和远见，能够做出艰难决定。是引领他人的时刻。', advice: '发挥领导力，但也要倾听他人意见。' }, reversed: { keywords: ['专制', '冲动', '缺乏远见'], meaning: '可能过于专制或冲动，缺乏远见。需要反思领导方式。', advice: '学会倾听，三思而后行。' } },

    // ========== 圣杯组（水元素）- 36-49 ==========
    36: { name: '圣杯 Ace', suit: 'cups', upright: { keywords: ['新感情', '爱', '直觉'], meaning: '新的感情或情感体验开始，充满爱和直觉。这是打开心扉的时期。', advice: '敞开心扉，接受新的情感体验。' }, reversed: { keywords: ['情感阻塞', '空虚', '压抑'], meaning: '可能感到情感阻塞或空虚，压抑自己的感受。需要释放。', advice: '允许自己感受情绪，寻求情感支持。' } },
    37: { name: '圣杯 2', suit: 'cups', upright: { keywords: ['关系', '合作', '平衡'], meaning: '一段平衡和谐的关系，可能是爱情或合作伙伴关系。彼此吸引，互相尊重。', advice: '珍惜这段关系，保持平等和尊重。' }, reversed: { keywords: ['关系问题', '不平衡', '分离'], meaning: '关系可能出现不平衡或问题，甚至面临分离。需要沟通。', advice: '坦诚沟通，寻找平衡点。' } },
    38: { name: '圣杯 3', suit: 'cups', upright: { keywords: ['庆祝', '友谊', '欢乐'], meaning: '与朋友一起庆祝，享受欢乐时光。这是社交和分享快乐的时期。', advice: '与亲友分享喜悦，享受当下。' }, reversed: { keywords: ['过度享乐', '孤立', '冲突'], meaning: '可能过度享乐，或感到孤立。朋友间可能有冲突。', advice: '适度享乐，修复友谊。' } },
    39: { name: '圣杯 4', suit: 'cups', upright: { keywords: ['不满', '沉思', '机会'], meaning: '对现状感到不满，沉思中。可能忽略了身边的机会。', advice: '重新评估现状，留意身边的机会。' }, reversed: { keywords: ['觉醒', '接受', '新机会'], meaning: '从沉思中觉醒，愿意接受新机会。开始积极行动。', advice: '抓住机会，走出舒适区。' } },
    40: { name: '圣杯 5', suit: 'cups', upright: { keywords: ['失落', '悲伤', '遗憾'], meaning: '感到失落和悲伤，专注于失去的东西。需要时间疗伤。', advice: '允许自己悲伤，但不要沉溺。看看还拥有什么。' }, reversed: { keywords: ['恢复', '接受', '希望'], meaning: '开始从悲伤中恢复，接受现实。看到希望。', advice: '放下过去，面向未来。' } },
    41: { name: '圣杯 6', suit: 'cups', upright: { keywords: ['怀旧', '童年', '纯真'], meaning: '怀念过去的美好时光，可能是童年或旧关系。感受纯真和快乐。', advice: '珍惜美好回忆，但不要沉溺过去。' }, reversed: { keywords: ['放下过去', '成长', '现实'], meaning: '需要放下过去，面对现实。已经准备好成长。', advice: '拥抱现在，面向未来。' } },
    42: { name: '圣杯 7', suit: 'cups', upright: { keywords: ['选择', '幻想', '梦想'], meaning: '面临多个选择，但可能被幻想迷惑。需要看清现实。', advice: '区分幻想和现实，做出明智选择。' }, reversed: { keywords: ['清晰', '决定', '现实'], meaning: '从幻想中清醒，看清现实。准备好做决定。', advice: '聚焦一个目标，付诸行动。' } },
    43: { name: '圣杯 8', suit: 'cups', upright: { keywords: ['离开', '寻找', '放下'], meaning: '你决定离开不满足的情况，寻找更深层的意义。这是勇敢放手的时刻。', advice: '相信自己的直觉，勇敢追寻。' }, reversed: { keywords: ['犹豫', '害怕离开', '停滞'], meaning: '可能犹豫不决，害怕离开熟悉的环境。需要勇气。', advice: '评估是否值得留下，鼓起勇气改变。' } },
    44: { name: '圣杯 9', suit: 'cups', upright: { keywords: ['满足', '快乐', '愿望'], meaning: '感到满足和快乐，愿望达成。这是享受成果的时刻。', advice: '享受当下，感恩所拥有的。' }, reversed: { keywords: ['不满足', '贪婪', '虚荣'], meaning: '可能感到不满足，或过于贪婪。需要调整心态。', advice: '学会知足，珍惜已有。' } },
    45: { name: '圣杯 10', suit: 'cups', upright: { keywords: ['幸福', '家庭', '圆满'], meaning: '家庭幸福，情感圆满。这是和谐美满的时刻。', advice: '珍惜家人，维护和谐关系。' }, reversed: { keywords: ['家庭问题', '不和谐', '分离'], meaning: '家庭可能出现问题或不和谐。需要修复关系。', advice: '坦诚沟通，修复关系。' } },
    46: { name: '圣杯侍从', suit: 'cups', upright: { keywords: ['敏感', '直觉', '新感情'], meaning: '敏感且富有直觉，可能开始新感情。愿意表达情感。', advice: '跟随直觉，表达真实感受。' }, reversed: { keywords: ['情绪化', '依赖', '压抑'], meaning: '可能过于情绪化或依赖他人。或压抑情感。', advice: '平衡情感，保持独立。' } },
    47: { name: '圣杯骑士', suit: 'cups', upright: { keywords: ['浪漫', '追求', '魅力'], meaning: '充满浪漫和魅力，追求爱情或理想。是表达情感的时期。', advice: '真诚表达情感，但也要现实。' }, reversed: { keywords: ['花心', '欺骗', '情绪化'], meaning: '可能花心或情绪化，或存在欺骗。需要诚实。', advice: '诚实面对自己和他人。' } },
    48: { name: '圣杯皇后', suit: 'cups', upright: { keywords: ['同情', '直觉', '滋养'], meaning: '充满同情心和直觉，善于滋养他人。是照顾他人的时刻。', advice: '发挥你的同情心，但也要照顾自己。' }, reversed: { keywords: ['过度牺牲', '情绪化', '依赖'], meaning: '可能过度牺牲自己，或过于情绪化。需要平衡。', advice: '设立边界，照顾自己的需求。' } },
    49: { name: '圣杯国王', suit: 'cups', upright: { keywords: ['智慧', '平衡', '控制'], meaning: '情感成熟且智慧，能够平衡情感和理性。是情感领袖。', advice: '发挥你的智慧，帮助他人。' }, reversed: { keywords: ['情绪化', '控制', '冷漠'], meaning: '可能情绪化或试图控制，或变得冷漠。需要平衡。', advice: '找到情感和理性的平衡。' } },

    // ========== 宝剑组（风元素）- 50-63 ==========
    50: { name: '宝剑 Ace', suit: 'swords', upright: { keywords: ['清晰', '真理', '突破'], meaning: '思想清晰，看到真理。这是突破和新的开始的时刻。', advice: '运用清晰的思维，做出明智决定。' }, reversed: { keywords: ['混乱', '困惑', '破坏'], meaning: '可能感到混乱和困惑，或有破坏性想法。需要冷静。', advice: '冷静下来，理清思路。' } },
    51: { name: '宝剑 2', suit: 'swords', upright: { keywords: ['选择', '僵局', '平衡'], meaning: '面临艰难选择，陷入僵局。需要平衡不同观点。', advice: '收集信息，做出决定。不要逃避。' }, reversed: { keywords: ['决定', '打破僵局', '情绪'], meaning: '准备好做决定，打破僵局。情绪可能影响判断。', advice: '相信直觉，做出选择。' } },
    52: { name: '宝剑 3', suit: 'swords', upright: { keywords: ['心痛', '悲伤', '分离'], meaning: '经历心痛和悲伤，可能是分离或背叛。需要时间疗伤。', advice: '允许自己悲伤，寻求支持。时间会治愈。' }, reversed: { keywords: ['恢复', '宽恕', '愈合'], meaning: '开始从心痛中恢复，愿意宽恕。正在愈合。', advice: '继续愈合过程，放下过去。' } },
    53: { name: '宝剑 4', suit: 'swords', upright: { keywords: ['休息', '恢复', '沉思'], meaning: '需要休息和恢复，暂时退出战斗。这是沉思和内省的时期。', advice: '给自己时间休息，恢复能量。' }, reversed: { keywords: ['恢复行动', '疲惫', '焦虑'], meaning: '休息后准备重新行动，或感到疲惫焦虑。', advice: '逐步恢复活动，不要操之过急。' } },
    54: { name: '宝剑 5', suit: 'swords', upright: { keywords: ['冲突', '胜利', '代价'], meaning: '卷入冲突，可能获得胜利但付出代价。需要权衡。', advice: '考虑是否值得争斗，有时退让更好。' }, reversed: { keywords: ['和解', '失败', '后悔'], meaning: '可能寻求和解，或感到失败和后悔。', advice: '寻求和解，放下仇恨。' } },
    55: { name: '宝剑 6', suit: 'swords', upright: { keywords: ['过渡', '治愈', '前进'], meaning: '正在度过困难时期，走向更好的地方。这是过渡和治愈的时刻。', advice: '继续前进，更好的日子在前方。' }, reversed: { keywords: ['停滞', '无法前进', '返回'], meaning: '可能停滞不前，或想返回过去。需要勇气。', advice: '放下过去，勇敢前进。' } },
    56: { name: '宝剑 7', suit: 'swords', upright: { keywords: ['策略', '欺骗', '秘密'], meaning: '需要策略和技巧，或存在欺骗和秘密。要小心行事。', advice: '谨慎行事，但不要走捷径。' }, reversed: { keywords: ['坦白', '面对', '改变策略'], meaning: '准备坦白或面对现实。需要改变策略。', advice: '诚实面对，改变方法。' } },
    57: { name: '宝剑 8', suit: 'swords', upright: { keywords: ['束缚', '限制', '无助'], meaning: '感到被束缚和限制，无助。但束缚往往是自我施加的。', advice: '认识到你有力量打破束缚。' }, reversed: { keywords: ['自由', '解放', '觉醒'], meaning: '开始从束缚中解放，认识到自己的力量。', advice: '勇敢迈出第一步，获得自由。' } },
    58: { name: '宝剑 9', suit: 'swords', upright: { keywords: ['焦虑', '恐惧', '噩梦'], meaning: '被焦虑和恐惧困扰，可能做噩梦。需要面对恐惧。', advice: '寻求支持，不要独自承受。恐惧往往不真实。' }, reversed: { keywords: ['恢复', '面对恐惧', '希望'], meaning: '开始从焦虑中恢复，勇敢面对恐惧。', advice: '继续面对恐惧，寻求专业帮助。' } },
    59: { name: '宝剑 10', suit: 'swords', upright: { keywords: ['结束', '背叛', '最低点'], meaning: '到达最低点，可能感到被背叛。但这也是结束和新的开始。', advice: '接受结束，寻求支持。情况会好转。' }, reversed: { keywords: ['恢复', '重生', '好转'], meaning: '开始从最低点恢复，看到希望。正在重生。', advice: '继续恢复，相信未来会更好。' } },
    60: { name: '宝剑侍从', suit: 'swords', upright: { keywords: ['好奇', '警惕', '新想法'], meaning: '充满好奇心，警惕周围。有新想法想要探索。', advice: '保持好奇，但也要谨慎。' }, reversed: { keywords: ['多疑', '八卦', '欺骗'], meaning: '可能过于多疑或参与八卦。或存在欺骗。', advice: '保持开放心态，避免八卦。' } },
    61: { name: '宝剑骑士', suit: 'swords', upright: { keywords: ['行动', '果断', '直接'], meaning: '行动迅速果断，直接追求目标。是高效执行的时期。', advice: '保持效率，但也要考虑他人感受。' }, reversed: { keywords: ['鲁莽', '攻击性', '混乱'], meaning: '可能过于鲁莽或有攻击性，导致混乱。', advice: '冷静下来，三思而后行。' } },
    62: { name: '宝剑皇后', suit: 'swords', upright: { keywords: ['独立', '清晰', '公正'], meaning: '独立且思维清晰，公正客观。能够做出艰难决定。', advice: '发挥你的判断力，但也要有同情心。' }, reversed: { keywords: ['冷酷', '苛刻', '偏见'], meaning: '可能过于冷酷或苛刻，或有偏见。需要平衡。', advice: '加入同情心，避免过于苛刻。' } },
    63: { name: '宝剑国王', suit: 'swords', upright: { keywords: ['权威', '逻辑', '判断'], meaning: '具有权威和强大的逻辑思维，能够做出公正判断。是领导时刻。', advice: '运用你的智慧，但也要倾听他人。' }, reversed: { keywords: ['专制', '无情', '操纵'], meaning: '可能过于专制或无情，或试图操纵。需要反思。', advice: '学会倾听，展现同情心。' } },

    // ========== 星币组（土元素）- 64-77 ==========
    64: { name: '星币 Ace', suit: 'pentacles', upright: { keywords: ['新机会', '财富', '实际'], meaning: '新的财务或事业机会出现，实际可行。这是播种的时期。', advice: '抓住机会，制定实际计划。' }, reversed: { keywords: ['错失机会', '浪费', '不实际'], meaning: '可能错失机会或浪费资源。计划不切实际。', advice: '重新评估计划，更加实际。' } },
    65: { name: '星币 2', suit: 'pentacles', upright: { keywords: ['平衡', '适应', '多任务'], meaning: '需要平衡多个责任或项目，适应变化。是灵活应对的时期。', advice: '保持灵活，合理分配时间。' }, reversed: { keywords: ['失衡', '压力', '混乱'], meaning: '可能失去平衡，感到压力和混乱。需要调整。', advice: '优先排序，寻求支持。' } },
    66: { name: '星币 3', suit: 'pentacles', upright: { keywords: ['合作', '技能', '学习'], meaning: '通过合作和学习技能获得成功。是团队工作的时期。', advice: '与他人合作，提升技能。' }, reversed: { keywords: ['缺乏合作', '技能不足', '冲突'], meaning: '可能缺乏合作或技能不足。团队可能有冲突。', advice: '改善沟通，提升技能。' } },
    67: { name: '星币 4', suit: 'pentacles', upright: { keywords: ['保守', '稳定', '控制'], meaning: '注重保守和稳定，控制资源。可能过于吝啬。', advice: '平衡保守和开放，适当分享。' }, reversed: { keywords: ['浪费', '失控', '慷慨'], meaning: '可能浪费或失去控制，或变得过于慷慨。', advice: '建立健康的财务习惯。' } },
    68: { name: '星币 5', suit: 'pentacles', upright: { keywords: ['困难', '损失', '孤立'], meaning: '经历财务困难或损失，感到孤立。需要寻求帮助。', advice: '寻求支持，不要独自承受。困难会过去。' }, reversed: { keywords: ['恢复', '希望', '帮助'], meaning: '开始从困难中恢复，看到希望。获得帮助。', advice: '继续恢复，接受帮助。' } },
    69: { name: '星币 6', suit: 'pentacles', upright: { keywords: ['分享', '慷慨', '平衡'], meaning: '分享资源，慷慨助人。给予和接受之间保持平衡。', advice: '慷慨分享，但也要接受他人帮助。' }, reversed: { keywords: ['不平等', '依赖', '吝啬'], meaning: '可能存在不平等或依赖关系。或过于吝啬。', advice: '建立平等关系，学会分享。' } },
    70: { name: '星币 7', suit: 'pentacles', upright: { keywords: ['耐心', '投资', '等待'], meaning: '播下种子后耐心等待收获。是评估进展的时刻。', advice: '保持耐心，继续努力。收获会到来。' }, reversed: { keywords: ['不耐烦', '延迟', '失望'], meaning: '可能感到不耐烦或失望，收获延迟。', advice: '重新评估策略，保持耐心。' } },
    71: { name: '星币 8', suit: 'pentacles', upright: { keywords: ['技能', '专注', '工艺'], meaning: '专注于提升技能和工艺，努力工作。是精进的时期。', advice: '继续精进，注重细节。' }, reversed: { keywords: ['分心', '懒惰', '缺乏进步'], meaning: '可能分心或懒惰，缺乏进步。需要重新聚焦。', advice: '重新聚焦目标，避免分心。' } },
    72: { name: '星币 9', suit: 'pentacles', upright: { keywords: ['成功', '独立', '享受'], meaning: '获得财务成功，享受独立和舒适。是奖励自己的时刻。', advice: '享受成果，但也要回馈社会。' }, reversed: { keywords: ['过度消费', '依赖', '不满足'], meaning: '可能过度消费或依赖他人。或感到不满足。', advice: '学会知足，建立独立性。' } },
    73: { name: '星币 10', suit: 'pentacles', upright: { keywords: ['财富', '家庭', '传承'], meaning: '获得长期财富和家庭稳定。考虑传承和遗产。', advice: '珍惜家庭，规划未来。' }, reversed: { keywords: ['家庭冲突', '财务问题', '损失'], meaning: '家庭可能有冲突或财务问题。需要解决。', advice: '坦诚沟通，解决问题。' } },
    74: { name: '星币侍从', suit: 'pentacles', upright: { keywords: ['学习', '机会', '实际'], meaning: '学习新技能或发现新机会。态度实际且勤奋。', advice: '抓住学习机会，脚踏实地。' }, reversed: { keywords: ['懒惰', '浪费', '不切实际'], meaning: '可能懒惰或浪费机会。计划不切实际。', advice: '制定实际计划，立即行动。' } },
    75: { name: '星币骑士', suit: 'pentacles', upright: { keywords: ['勤奋', '可靠', '耐心'], meaning: '勤奋可靠，耐心追求目标。是稳步前进的时期。', advice: '继续保持勤奋，不要急躁。' }, reversed: { keywords: ['懒惰', '固执', '停滞'], meaning: '可能变得懒惰或固执，进展停滞。', advice: '重新激发动力，灵活应对。' } },
    76: { name: '星币皇后', suit: 'pentacles', upright: { keywords: ['滋养', '实际', '繁荣'], meaning: '善于滋养他人和自己，创造繁荣。是照顾的时刻。', advice: '发挥你的滋养能力，创造舒适环境。' }, reversed: { keywords: ['过度保护', '物质主义', '忽视'], meaning: '可能过度保护或过于物质主义。或忽视自己。', advice: '平衡物质和精神需求。' } },
    77: { name: '星币国王', suit: 'pentacles', upright: { keywords: ['成功', '领导', '稳定'], meaning: '获得财务成功和稳定，具有领导力。是指导他人的时刻。', advice: '运用你的经验，帮助他人成功。' }, reversed: { keywords: ['贪婪', '固执', '腐败'], meaning: '可能变得贪婪或固执，或存在腐败。需要反思。', advice: '重新审视价值观，保持正直。' } }
};

/**
 * 获取牌的基本含义
 */
function getBaseCardMeaning(cardId, position) {
    // 大阿卡纳
    if (cardId < 22) {
        const meaning = majorArcana[cardId];
        if (meaning) {
            return position === 'upright' ? meaning.upright : meaning.reversed;
        }
    }
    
    // 小阿卡纳
    if (cardId >= 22 && cardId <= 77) {
        const meaning = minorArcana[cardId];
        if (meaning) {
            return position === 'upright' ? meaning.upright : meaning.reversed;
        }
    }
    
    // 默认返回（不应该发生）
    return {
        keywords: ['探索', '成长', '启示'],
        meaning: '这张牌邀请你深入探索当下的情况，保持开放的心态。',
        advice: '相信自己的直觉，答案会在适当的时候出现。'
    };
}

/**
 * 生成三张牌的综合解读
 */
function generateSummary(cards) {
    const cardNames = cards.map(c => c.name).join(' → ');
    const uprightCount = cards.filter(c => c.position === 'upright').length;
    const reversedCount = cards.length - uprightCount;
    
    let summary = `<p><strong>🎴 牌阵：</strong>${cardNames}</p>`;
    summary += `<p><strong>✨ 能量分布：</strong>正位${uprightCount}张 · 逆位${reversedCount}张</p>`;
    summary += `<hr style="border:0; border-top:1px solid rgba(144,202,249,0.3); margin:15px 0;">`;
    
    summary += `<h4 style="color:#64b5f6; margin:15px 0 10px;">📖 整体解读</h4>`;
    
    if (uprightCount >= 2) {
        summary += `<p>整体能量偏向积极正面，显示你当前的情况正在向好的方向发展。大部分牌的正位表明你具备解决问题所需的资源和能力。</p>`;
    } else if (reversedCount >= 2) {
        summary += `<p>整体能量显示存在一些阻碍和挑战，需要你先解决内在的问题或调整心态。逆位牌提醒你注意潜在的陷阱。</p>`;
    } else {
        summary += `<p>正逆位能量相对平衡，表明情况既有积极面也有挑战。关键在于如何平衡和转化这些能量。</p>`;
    }
    
    summary += `<h4 style="color:#64b5f6; margin:15px 0 10px;">⏰ 时间流分析</h4>`;
    summary += `<p><strong>过去（${cards[0].name}）：</strong>影响你当前状况的过去因素。</p>`;
    summary += `<p><strong>现在（${cards[1].name}）：</strong>你当前的核心状态和挑战。</p>`;
    summary += `<p><strong>未来（${cards[2].name}）：</strong>如果保持当前轨迹，可能的发展方向。</p>`;
    
    summary += `<h4 style="color:#ffb74d; margin:15px 0 10px;">🎯 核心建议</h4>`;
    const allKeywords = cards.flatMap(c => getBaseCardMeaning(c.id, c.position).keywords.slice(0,2));
    const uniqueKeywords = [...new Set(allKeywords)].slice(0, 5);
    summary += `<p>综合三张牌的指引，建议你关注：<strong>${uniqueKeywords.join(' · ')}</strong>。</p>`;
    summary += `<p style="margin-top:15px; color:#e3f2fd; font-style:italic;">🔮 记住，塔罗牌是帮助你了解自己的工具，最终的选择权在你手中。</p>`;
    
    return summary;
}
