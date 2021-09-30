	.file	"staticStack.c"
	.text
	.section	.rodata
.LC0:
	.string	"Welcome to my stack! :)"
	.align 8
.LC1:
	.string	"\nSelect working regime or try 'q' for quit: "
.LC2:
	.string	"\nAre you polish?"
.LC3:
	.string	"\nGoodnight, sweet prince."
	.text
	.globl	main
	.type	main, @function
main:
.LFB0:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$112, %rsp
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	leaq	-96(%rbp), %rdx
	movl	$0, %eax
	movl	$10, %ecx
	movq	%rdx, %rdi
	rep stosq
	movq	%rdi, %rdx
	movl	%eax, (%rdx)
	addq	$4, %rdx
	movb	$-1, -96(%rbp)
	leaq	.LC0(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	call	printHelp
.L13:
	leaq	.LC1(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	jmp	.L2
.L3:
	nop
.L2:
	call	getchar@PLT
	movb	%al, -97(%rbp)
	cmpb	$10, -97(%rbp)
	je	.L3
	movsbl	-97(%rbp), %eax
	subl	$104, %eax
	cmpl	$12, %eax
	ja	.L4
	movl	%eax, %eax
	leaq	0(,%rax,4), %rdx
	leaq	.L6(%rip), %rax
	movl	(%rdx,%rax), %eax
	cltq
	leaq	.L6(%rip), %rdx
	addq	%rdx, %rax
	notrack jmp	*%rax
	.section	.rodata
	.align 4
	.align 4
.L6:
	.long	.L11-.L6
	.long	.L4-.L6
	.long	.L4-.L6
	.long	.L10-.L6
	.long	.L9-.L6
	.long	.L4-.L6
	.long	.L4-.L6
	.long	.L4-.L6
	.long	.L8-.L6
	.long	.L16-.L6
	.long	.L4-.L6
	.long	.L4-.L6
	.long	.L5-.L6
	.text
.L11:
	leaq	-96(%rbp), %rax
	movq	%rax, %rdi
	call	push
	jmp	.L12
.L8:
	leaq	-96(%rbp), %rax
	movq	%rax, %rdi
	call	pop
	jmp	.L12
.L10:
	leaq	-96(%rbp), %rax
	movq	%rax, %rdi
	call	peek
	jmp	.L12
.L5:
	leaq	-96(%rbp), %rax
	movq	%rax, %rdi
	call	printStack
	jmp	.L12
.L9:
	call	printHelp
	jmp	.L12
.L4:
	leaq	.LC2(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	jmp	.L12
.L16:
	nop
.L12:
	cmpb	$113, -97(%rbp)
	jne	.L13
	leaq	.LC3(%rip), %rdi
	call	puts@PLT
	movl	$0, %eax
	movq	-8(%rbp), %rsi
	xorq	%fs:40, %rsi
	je	.L15
	call	__stack_chk_fail@PLT
.L15:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	main, .-main
	.section	.rodata
.LC4:
	.string	"\nStack is full"
.LC5:
	.string	"\nPut data for push: "
.LC6:
	.string	"%d"
	.text
	.globl	push
	.type	push, @function
push:
.LFB1:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$32, %rsp
	movq	%rdi, -24(%rbp)
	movq	%fs:40, %rax
	movq	%rax, -8(%rbp)
	xorl	%eax, %eax
	movq	-24(%rbp), %rax
	movzbl	(%rax), %eax
	cmpb	$19, %al
	jne	.L18
	leaq	.LC4(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	jmp	.L17
.L18:
	leaq	.LC5(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	-12(%rbp), %rax
	movq	%rax, %rsi
	leaq	.LC6(%rip), %rdi
	movl	$0, %eax
	call	__isoc99_scanf@PLT
	movq	-24(%rbp), %rax
	movzbl	(%rax), %eax
	addl	$1, %eax
	movl	%eax, %edx
	movq	-24(%rbp), %rax
	movb	%dl, (%rax)
	movq	-24(%rbp), %rax
	movzbl	(%rax), %eax
	movsbl	%al, %edx
	movl	-12(%rbp), %ecx
	movq	-24(%rbp), %rax
	movslq	%edx, %rdx
	movl	%ecx, 4(%rax,%rdx,4)
	movq	-24(%rbp), %rax
	movq	%rax, %rdi
	call	printStack
	nop
.L17:
	movq	-8(%rbp), %rax
	xorq	%fs:40, %rax
	je	.L21
	call	__stack_chk_fail@PLT
.L21:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE1:
	.size	push, .-push
	.section	.rodata
.LC7:
	.string	"\nStack is empty"
	.text
	.globl	pop
	.type	pop, @function
pop:
.LFB2:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movzbl	(%rax), %eax
	testb	%al, %al
	jns	.L23
	leaq	.LC7(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	jmp	.L22
.L23:
	movq	-8(%rbp), %rax
	movzbl	(%rax), %eax
	movsbl	%al, %edx
	movq	-8(%rbp), %rax
	movslq	%edx, %rdx
	movl	$0, 4(%rax,%rdx,4)
	movq	-8(%rbp), %rax
	movzbl	(%rax), %eax
	subl	$1, %eax
	movl	%eax, %edx
	movq	-8(%rbp), %rax
	movb	%dl, (%rax)
	movq	-8(%rbp), %rax
	movq	%rax, %rdi
	call	printStack
	nop
.L22:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE2:
	.size	pop, .-pop
	.section	.rodata
.LC8:
	.string	"\nPeeking data: %d"
	.text
	.globl	peek
	.type	peek, @function
peek:
.LFB3:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$16, %rsp
	movq	%rdi, -8(%rbp)
	movq	-8(%rbp), %rax
	movzbl	(%rax), %eax
	testb	%al, %al
	jns	.L27
	leaq	.LC7(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	jmp	.L26
.L27:
	movq	-8(%rbp), %rax
	movzbl	(%rax), %eax
	movsbl	%al, %edx
	movq	-8(%rbp), %rax
	movslq	%edx, %rdx
	movl	4(%rax,%rdx,4), %eax
	movl	%eax, %esi
	leaq	.LC8(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movq	-8(%rbp), %rax
	movq	%rax, %rdi
	call	printStack
	nop
.L26:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE3:
	.size	peek, .-peek
	.section	.rodata
.LC9:
	.string	"\nActual size: %d"
.LC10:
	.string	"\nCurrent data: "
.LC11:
	.string	"%d "
	.text
	.globl	printStack
	.type	printStack, @function
printStack:
.LFB4:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	subq	$32, %rsp
	movq	%rdi, -24(%rbp)
	movq	-24(%rbp), %rax
	movzbl	(%rax), %eax
	testb	%al, %al
	jns	.L31
	leaq	.LC7(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	jmp	.L30
.L31:
	movq	-24(%rbp), %rax
	movzbl	(%rax), %eax
	movsbl	%al, %eax
	addl	$1, %eax
	movl	%eax, %esi
	leaq	.LC9(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	leaq	.LC10(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movb	$0, -1(%rbp)
	jmp	.L33
.L34:
	movq	-24(%rbp), %rax
	movzbl	(%rax), %eax
	movsbl	%al, %edx
	movsbl	-1(%rbp), %eax
	subl	%eax, %edx
	movq	-24(%rbp), %rax
	movslq	%edx, %rdx
	movl	4(%rax,%rdx,4), %eax
	movl	%eax, %esi
	leaq	.LC11(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	movzbl	-1(%rbp), %eax
	addl	$1, %eax
	movb	%al, -1(%rbp)
.L33:
	movq	-24(%rbp), %rax
	movzbl	(%rax), %eax
	cmpb	%al, -1(%rbp)
	jle	.L34
	nop
.L30:
	leave
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE4:
	.size	printStack, .-printStack
	.section	.rodata
	.align 8
.LC12:
	.string	"\nWhat can i do:\n\t- 'h' for push\n\t- 'p' for pop\n\t- 'k' for peek \n\t- 't' for just print\n\t- 'l' for help"
	.text
	.globl	printHelp
	.type	printHelp, @function
printHelp:
.LFB5:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	leaq	.LC12(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	nop
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE5:
	.size	printHelp, .-printHelp
	.ident	"GCC: (Ubuntu 9.3.0-17ubuntu1~20.04) 9.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	 1f - 0f
	.long	 4f - 1f
	.long	 5
0:
	.string	 "GNU"
1:
	.align 8
	.long	 0xc0000002
	.long	 3f - 2f
2:
	.long	 0x3
3:
	.align 8
4:
