vim.opt.title = true
vim.opt.hidden = true
vim.opt.number = true
vim.opt.ambiwidth = "double"
vim.opt.selection = "exclusive"
vim.opt.virtualedit = "onemore"
vim.opt.whichwrap = "b", "s", "h", "l", "<", ">", "[", "]"
vim.opt.incsearch = true

vim.keymap.set("i", "<C-j>", "<C-o>")

vim.api.nvim_create_autocmd("VimLeave", {
  callback = function()
    os.execute("echo -ne '\\033]0;\\007'")
  end,
})
