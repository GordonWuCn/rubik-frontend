#

from rubik import *


class ip_header_layout(layout):
    srcip = Bit(32)
    dstip = Bit(32)


class ip_header_layout2(layout):
    pass


class ip_header_layout3(layout):
    pass


class op1(layout):
    type_id = Bit(16, const=0x1)
    port = Bit(16)
    option_len = Bit(16)
    option = Bit(option_len << 2)


class op2(layout):
    type_id = Bit(16, const=0x0)


class op3(layout):
    type_id = Bit(16, const=0x42)
    dummy = Bit(128)


def ip_parser():
    ip = Connectionless()
    ip.header = ip_header_layout
    ip.header += If(ip.header.srcip ==
                    1) >> ip_header_layout2 >> Else() >> ip_header_layout3
    ip.header += While(ip.cursor <
                       ip.header.option_len) >> Any(op1, op2, op3)
    # ip.selector = ([ip.header.srcip], [ip.header.dstip])
    # ip.temp = ip_temp_layout
    # ip.preprocess = Assign(ip.temp.offset, ((ip.header.f1 << 8) + ip.header.f2) << 3)
    # ip.seq = Sequence(meta=ip.temp.offset, data=ip.payload, data_len=ip.payload_len)
    # DUMP = PSMState(start=True, accept=True)
    # FRAG, OTHER1, OTHER2 = PSMState(3)
    # ip.psm = PSM(DUMP, FRAG)
    # ip.psm.dump = DUMP >> DUMP + Predicate(ip.header.dont_frag == 1)
    # ip.psm.frag = DUMP >> FRAG + Predicate(ip.header.more_frag == 1)
    # ip.psm.more = FRAG >> FRAG + Predicate(ip.header.more_frag == 1)
    # ip.psm.last = FRAG >> DUMP + Predicate(ip.v.header.more_frag == 0)
    # ip.event.assemble = If(ip.psm.dump or ip.psm.last) >> ip.seq.assemble()
    return ip

# # user defined event demo
# ip = ip_parser()
# ip.event.on_every = If(true) >> Assign(on_every_layout.srcip, on_every_layout.srcip) + callback(on_every_layout)


# stack = Stack()
# stack.eth = eth
# stack.ip = stack.eth >> ip_parser()
# stack.udp = stack.ip >> If(
#     (stack.ip.psm.last or stack.ip.psm.dump) and stack.ip.header.protocol == 17
# ) >> udp
# stack.gtp = stack.udp >> gtp
# stack.gtp_ip = stack.gtp >> If(stack.gtp.header.MT == 255) >> ip_parser()
# gtp_ip_dump = stack.gtp_ip.psm.last or stack.gtp_ip.psm.dump
# stack.gtp_tcp = stack.gtp_ip >> If(gtp_ip_dump and stack.gtp_ip.header.protocol == 6) >> tcp
# stack.gtp_udp = stack.gtp_ip >> If(gtp_ip_dump and stack.gtp_ip.header.protocol == 17) >> udp

# class on_every_high_udp_layout(layout):
#     srcip = bit(32)
#     dstip = bit(32)
# stack.event.on_every_high_udp = If(stack.gtp_udp) >> Assign(...) + callback(on_every_high_udp_layout)

#
# In [1]: from ip import ip_parser

# In [2]: p = ip_parser()

# In [3]: p.header
# Out[3]: <rubik.layout.SeqLayout at 0x1aaf989df60>

# In [4]: p.header.layout_list
# Out[4]: 
# [<rubik.layout.StructLayout at 0x1aaf989da58>,
#  <rubik.layout.IfElseLayout at 0x1aaf989da90>,
#  <rubik.layout.WhileAnyLayout at 0x1aaf989df98>]

# In [5]: p.header.layout_list[1].true
# Out[5]: <rubik.layout.StructLayout at 0x1aaf989dc88>

# In [6]: p.header.layout_list[2].choice_list
# Out[6]: 
# [<rubik.layout.StructLayout at 0x1aaf989dfd0>,
#  <rubik.layout.StructLayout at 0x1aaf98c6048>,
#  <rubik.layout.StructLayout at 0x1aaf98c6080>]

# In [7]: p.header.layout_list[2].prefix_length
# Out[7]: 16

# In [8]: p.header.layout_list[2].choice_list[0].iter_field()
# Out[8]: <generator object StructLayout.iter_field at 0x000001AAF97CDCF0>

# In [9]: list(p.header.layout_list[2].choice_list[0].iter_field())
# Out[9]: 
# [('type_id', <rubik.layout.Bit at 0x1aaf9896a20>),
#  ('port', <rubik.layout.Bit at 0x1aaf9896a58>),
#  ('option_len', <rubik.layout.Bit at 0x1aaf9896a90>),
#  ('option', <rubik.layout.Bit at 0x1aaf98806d8>)]

# In [10]: list(p.header.layout_list[2].choice_list[0].iter_field())[3][1].const

# In [11]: list(p.header.layout_list[2].choice_list[0].iter_field())[3][1].length
# Out[11]: <rubik.expr.Op at 0x1aaf9896b00>

# In [12]: list(p.header.layout_list[2].choice_list[0].iter_field())[3][1].length.op
# Out[12]: 'lshift'

# In [13]: list(p.header.layout_list[2].choice_list[0].iter_field())[3][1].length.lhs
# Out[13]: <rubik.layout.Bit at 0x1aaf9896a90>

# In [14]: list(p.header.layout_list[2].choice_list[0].iter_field())[3][1].length.rhs
# Out[14]: 2